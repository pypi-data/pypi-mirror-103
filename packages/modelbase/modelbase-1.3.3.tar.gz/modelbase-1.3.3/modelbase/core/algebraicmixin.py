"""Mixin for algebraic modules. These are used to calculate e.g. QSSA assumptions."""
from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import Union, Callable

import numpy as np
import libsbml

from .utils import (
    get_formatted_function_source_code,
    patch_lambda_function_name,
    warning_on_one_line,
)

warnings.formatwarning = warning_on_one_line


@dataclass
class Module:
    """Meta-info container for an algebraic module."""

    common_name: str = None
    notes: dict = field(default_factory=dict)
    database_links: dict = field(default_factory=dict)


class AlgebraicMixin:
    """Mixin for algebraic modules.

    This adds the capability to calculate concentrations of derived
    compounds that are calculated before the rate functions are calculated.
    """

    def __init__(self, algebraic_modules: dict = None):
        self.algebraic_modules = {}
        if algebraic_modules is not None:
            self.add_algebraic_modules(algebraic_modules=algebraic_modules)

    ##########################################################################
    # Derived compound functions
    ##########################################################################

    def get_derived_compounds(self) -> list[str]:
        """Return names of compounds derived from algebraic modules."""
        derived_compounds = []
        for module in self.algebraic_modules.values():
            derived_compounds.extend(module["derived_compounds"])
        return derived_compounds

    @property
    def derived_compounds(self) -> list[str]:
        """Return names of compounds derived from algebraic modules

        Used to be an attribute of the model, so this is kept to ensure backwards compatability
        """
        return self.get_derived_compounds()

    def get_all_compounds(self) -> list[str]:
        """Return names of compounds and derived compounds (in that order)."""
        return list(self.get_compounds() + self.get_derived_compounds())

    ##########################################################################
    # Algebraic Modules
    ##########################################################################

    def add_algebraic_module(
        self,
        module_name: str,
        function: Callable,
        compounds: list[str] = None,
        derived_compounds: list[str] = None,
        modifiers: list[str] = None,
        parameters: list[str] = None,
        args: list[str] = None,
        **meta_info,
    ):
        """Add an algebraic module to the model.

        CAUTION: The Python function of the module has to return an iterable.
        The Python function will get the function arguments in the following order:
        [**compounds, **modifiers, **parameters]

        Warns
        -----
        UserWarning
            If algebraic module is already in the model.

        Examples
        --------
        def rapid_equilibrium(substrate, k_eq):
            x = substrate / (1 + k_eq)
            y = substrate * k_eq / (1 + k_eq)
            return x, y

        add_algebraic_module(
            module_name="fast_eq",
            function=rapid_equilibrium,
            compounds=["A"],
            derived_compounds=["X", "Y"],
            parameters=["K"],
        )
        """
        if compounds is None:
            compounds = []
        if derived_compounds is None:
            derived_compounds = []
        if modifiers is None:
            modifiers = []
        if parameters is None:
            parameters = []
        if args is None:
            args = compounds + modifiers + parameters

        if module_name in self.algebraic_modules:
            self.remove_algebraic_module(module_name=module_name)
            warnings.warn(f"Overwriting algebraic module {module_name}")

        self._check_for_existence(
            name=module_name, check_against=self.get_all_compounds(), candidates=compounds + modifiers
        )
        self._check_for_existence(
            name=module_name, check_against=self.get_parameter_names(), candidates=parameters
        )
        self._check_and_insert_ids(derived_compounds)

        patch_lambda_function_name(function=function, name=module_name)

        self.algebraic_modules[module_name] = {
            "function": function,
            "compounds": compounds,
            "derived_compounds": derived_compounds,
            "modifiers": modifiers,
            "parameters": parameters,
            "args": args,
        }

        self.meta_info.setdefault("modules", {}).setdefault(module_name, Module(**meta_info))

    def add_algebraic_modules(self, algebraic_modules: dict, meta_info: dict = None):
        """Add multiple algebraic modules to the model.

        See Also
        --------
        add_algebraic_module
        """
        meta_info = {} if meta_info is None else meta_info
        for module_name, module in algebraic_modules.items():
            info = meta_info.get(module_name, {})
            self.add_algebraic_module(module_name=module_name, **module, **info)

    def update_algebraic_module(
        self,
        module_name: str,
        function: Callable = None,
        compounds: list[str] = None,
        derived_compounds: list[str] = None,
        modifiers: list[str] = None,
        parameters: list[str] = None,
        args: list[str] = None,
    ):
        """Update an existing reaction."""
        module = self.algebraic_modules[module_name]
        args_have_changed = False
        if function is not None:
            patch_lambda_function_name(function=function, name=module_name)
            module["function"] = function
        if compounds is not None:
            module["compounds"] = compounds
            args_have_changed = True
        else:
            compounds = module["compounds"]
        if derived_compounds is not None:
            derived_changes = dict(zip(module["derived_compounds"], derived_compounds))
            self._update_ids(derived_changes)
            module["derived_compounds"] = derived_compounds
            args_have_changed = True
        if modifiers is not None:
            module["modifiers"] = modifiers
            args_have_changed = True
        else:
            modifiers = module["modifiers"]
        if parameters is not None:
            module["parameters"] = parameters
            args_have_changed = True
        else:
            parameters = module["parameters"]

        self._check_for_existence(
            name=module_name, check_against=self.get_all_compounds(), candidates=compounds + modifiers
        )
        self._check_for_existence(
            name=module_name, check_against=self.get_parameter_names(), candidates=parameters
        )

        if args is not None:
            module["args"] = args
        elif args_have_changed:
            module["args"] = compounds + modifiers + parameters

    def update_algebraic_modules(self, modules: dict):
        """Update multiple algebraic modules

        See Also
        --------
        update_algebraic_module
        """
        for name, module in modules.items():
            self.update_algebraic_module(name, **module)

    def update_module_meta_info(self, module: str, meta_info: dict):
        """Update meta info of an algebraic module.

        Parameters
        ----------
        module : str
            Name of the algebraic module
        meta_info : dict
            Meta info of the algebraic module. Allowed keys are
            {common_name, notes, database_links}
        """
        self.update_meta_info(component="modules", meta_info={module: meta_info})

    def remove_algebraic_module(self, module_name: str):
        """Remove an algebraic module.

        Parameters
        ----------
        module_name : str
            Name of the algebraic module
        """
        module = self.algebraic_modules.pop(module_name)
        self._remove_ids(module["derived_compounds"])

    def remove_algebraic_modules(self, module_names: list[str]):
        """Remove multiple algebraic modules.

        Parameters
        ----------
        module_names : iterable(str)
            Names of the algebraic modules
        """
        for module_name in module_names:
            self.remove_algebraic_module(module_name=module_name)

    def get_algebraic_module(self, module_name: str) -> dict:
        return self.algebraic_modules[module_name]

    def get_algebraic_module_function(self, module_name: str) -> callable:
        return self.algebraic_modules[module_name]["function"]

    def get_algebraic_module_compounds(self, module_name: str) -> list[str]:
        return list(self.algebraic_modules[module_name]["compounds"])

    def get_algebraic_module_derived_compounds(self, module_name: str) -> list[str]:
        return list(self.algebraic_modules[module_name]["derived_compounds"])

    def get_algebraic_module_modifiers(self, module_name: str) -> list[str]:
        return list(self.algebraic_modules[module_name]["modifiers"])

    def get_algebraic_module_parameters(self, module_name: str) -> list[str]:
        return list(self.algebraic_modules[module_name]["parameters"])

    def get_algebraic_module_args(self, module_name: str) -> list[str]:
        return list(self.algebraic_modules[module_name]["args"])

    ##########################################################################
    # Simulation functions
    ##########################################################################

    def _get_fcd(
        self,
        *,
        t: Union[float, list[float]],
        y: Union[dict[str, float], dict[str, list[float]]],
    ) -> Union[dict[str, float], dict[str, list[float]]]:
        """Calculate the derived variables of all algebraic modules.

        fdc = full_concentration_dict

        The derived compounds are sorted by the algebraic modules and their internal
        derived_modules attribute.
        """
        y["time"] = t
        # args = self.parameters | y # that is python 3.9+ syntax, wait for a bit
        args = {**self.parameters, **y}
        for name, module in self.algebraic_modules.items():
            try:
                derived_values = module["function"](*(args[arg] for arg in module["args"]))
            except KeyError as e:
                raise KeyError(f"Could not find argument {e} for module {name}")
            derived_compounds = dict(
                zip(
                    module["derived_compounds"],
                    np.array(derived_values).reshape((len(module["derived_compounds"]), -1)),
                )
            )
            y.update(derived_compounds)
            args.update(derived_compounds)
        return y

    ##########################################################################
    # Source code functions
    ##########################################################################

    def _generate_algebraic_modules_source_code(self, *, include_meta_info=True) -> tuple[str]:
        """Generate modelbase source code for algebraic modules.

        This is mainly used for the generate_model_source_code function.

        Parameters
        ----------
        include_meta_info : bool
            Whether to include meta info in the source code.

        Returns
        -------
        algebraic_module_source_code : str
            Code generating the Python functions of the algebraic modules
        algebraic_module_modelbase_code : str
            Code generating the modelbase objects

        See Also
        --------
        generate_model_source_code
        """
        module_functions = set()
        modules = []
        for name, module in self.algebraic_modules.items():
            function = module["function"]
            compounds = module["compounds"]
            derived_compounds = module["derived_compounds"]
            modifiers = module["modifiers"]
            parameters = module["parameters"]
            args = module["args"]

            function_code = get_formatted_function_source_code(
                function_name=name, function=function, function_type="module"
            )
            module_functions.add(function_code)
            module_definition = (
                "m.add_algebraic_module(\n"
                f"    module_name={repr(name)},\n"
                f"    function={function.__name__},\n"
                f"    compounds={compounds},\n"
                f"    derived_compounds={derived_compounds},\n"
                f"    modifiers={modifiers},\n"
                f"    parameters={parameters},\n"
                f"    args={args},\n"
            )
            if include_meta_info:
                meta_info = self._get_nonzero_meta_info(component="modules")
                try:
                    info = meta_info[name]
                    module_definition += f"**{info}"
                except KeyError:
                    pass
            module_definition += ")"
            modules.append(module_definition)
        return "\n".join(sorted(module_functions)), "\n".join(modules)

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _create_sbml_algebraic_modules(self, *, sbml_model: libsbml.Model):
        """Convert the algebraic modules their sbml equivalent.

        Notes
        -----
        The closest we can get in SBML are assignment rules of the form x = f(V), see
        http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_assignment_rule.html

        Thus we have to split algebraic modules that contain multiple derived compounds
        into multiple assignment rules.

        But apparently they do not support parameters, so for now I am skipping
        this.
        """
        warnings.warn("SBML does support algebraic modules, skipping.")
