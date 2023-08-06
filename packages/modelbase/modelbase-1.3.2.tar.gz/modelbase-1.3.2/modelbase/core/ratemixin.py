"""Mixin for rates."""
from __future__ import annotations

import warnings
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Union

import libsbml

from .utils import (
    convert_id_to_sbml,
    get_formatted_function_source_code,
    patch_lambda_function_name,
    warning_on_one_line,
)

warnings.formatwarning = warning_on_one_line


@dataclass
class Rate:
    """Meta-info container for rates."""

    common_name: str = None
    unit: str = None
    gibbs0: float = None
    ec: str = None
    database_links: dict = field(default_factory=dict)
    notes: dict = field(default_factory=dict)
    sbml_function: str = None
    python_function: str = None


class RateMixin:
    """Mixin adding rate functions."""

    def __init__(self, rates: dict = None, functions: dict = None):
        self.rates = {}
        self.functions = {}
        if rates is not None:
            self.add_rates(rates=rates)
        if functions is not None:
            self.add_functions(functions=functions)

    ##########################################################################
    # Basic rate functions
    ##########################################################################

    def add_function(self, function_name: str, function: callable):
        if function.__name__ == "<lambda>":
            patch_lambda_function_name(function=function, name=function_name)

        self.functions[function_name] = function

    def add_functions(self, functions: dict[str, callable]):
        for function_name, function in functions.items():
            self.add_function(function_name=function_name, function=function)

    def update_function(self, function_name: str, function: callable):
        if function.__name__ == "<lambda>":
            patch_lambda_function_name(function=function, name=function_name)
        self.functions[function_name] = function

    def update_functions(self, functions: dict[str, callable]):
        for function_name, function in functions.items():
            self.update_function(function_name, function)

    def remove_function(self, function_name: str):
        del self.functions[function_name]

    def remove_functions(self, function_names: list[str]):
        for function_name in function_names:
            self.remove_function(function_name)

    def add_rate(
        self,
        rate_name: str,
        function: callable,
        substrates: list[str] = None,
        products: list[str] = None,
        modifiers: list[str] = None,
        dynamic_variables: list[str] = None,
        parameters: list[str] = None,
        reversible: bool = False,
        args: list[str] = None,
        check_consistency: bool = True,
        **meta_info,
    ):
        """Add a rate function to the model.

        The Python function will get the function arguments in the following order:
        [**substrates, **(products if reversible), **modifiers, **parameters.]

        Parameters
        ----------
        rate_name
            Name of the rate function
        function
            Python method calculating the rate equation
        substrates
            Names of the substrates
        products
            Names of the products
        modifiers
            Names of the modifiers. E.g time.
        parameters
            Names of the parameters
        reversible
            Whether the reaction is reversible.
        meta_info
            Meta info of the rate. Allowed keys are
            {common_name, gibbs0, ec, database_links, notes, sbml_function}

        Warns
        -----
        UserWarning
            If rate is already in the model

        Examples
        --------
        def mass_action(S, k1):
            return k1 * S

        m.add_reaction(
            rate_name="v1",
            function=mass_action,
            stoichiometry={"X": -1},
            parameters=["k1"],
        )

        def reversible_mass_action(S, P, k_fwd, k_bwd):
            return k_fwd * S - k_bwd * P

        m.add_reaction(
            rate_name="v2",
            function=reversible_mass_action,
            stoichiometry={"X": -1, "Y": 1},
            parameters=["k2_fwd", "k2_bwd"],
            reversible=True,
        )
        """
        if substrates is None:
            substrates = []
        if products is None:
            products = []
        if parameters is None:
            parameters = []
        if modifiers is None:
            modifiers = []
        if dynamic_variables is None:
            if reversible:
                dynamic_variables = substrates + products + modifiers
            else:
                dynamic_variables = substrates + modifiers
        if args is None:
            args = dynamic_variables + parameters

        if check_consistency:
            self._check_for_existence(
                name=rate_name, check_against=self.get_all_compounds(), candidates=dynamic_variables
            )
            self._check_for_existence(
                name=rate_name, check_against=self.get_parameter_names(), candidates=parameters
            )

        patch_lambda_function_name(function=function, name=rate_name)

        if rate_name in self.rates:
            warnings.warn(f"Overwriting rate {rate_name}")
            self.remove_rate(rate_name=rate_name)
        self.rates[rate_name] = {
            "function": function,
            "parameters": parameters,
            "substrates": substrates,
            "products": products,
            "modifiers": modifiers,
            "reversible": reversible,
            "dynamic_variables": dynamic_variables,
            "args": args,
        }
        self.meta_info.setdefault("rates", {}).setdefault(rate_name, Rate(**meta_info))

    def add_rates(self, rates: dict, meta_info=None):
        """Add multiple rates to the model.

        See Also
        --------
        add_rate
        """
        meta_info = {} if meta_info is None else meta_info
        for rate_name, rate in rates.items():
            info = meta_info.get(rate_name, {})
            self.add_rate(rate_name=rate_name, **rate, **info)

    def update_rate(
        self,
        rate_name: str,
        function: callable = None,
        substrates: list[str] = None,
        products: list[str] = None,
        modifiers: list[str] = None,
        parameters: list[str] = None,
        reversible: bool = None,
        dynamic_variables: list[str] = None,
        args: list[str] = None,
        check_consistency: bool = True,
    ):
        """Update an existing rate.

        Parameters
        ----------
        rate_name
            Name of the rate function
        function
            Python method calculating the rate equation
        substrates
            Names of the substrates
        products
            Names of the products
        modifiers
            Names of the modifiers. E.g time.
        parameters
            Names of the parameters
        reversible
            Whether the reaction is reversible.
        meta_info
            Meta info of the rate. Allowed keys are
            {common_name, gibbs0, ec, database_links, notes, sbml_function}

        See Also
        --------
        add_rate
        """
        rate = self.rates[rate_name]
        reversible_changed = False
        args_have_changed = False

        if function is not None:
            patch_lambda_function_name(function=function, name=rate_name)
            rate["function"] = function
        if substrates is not None:
            args_have_changed = True
            rate["substrates"] = substrates
        else:
            substrates = rate["substrates"]
        if products is not None:
            args_have_changed = True
            rate["products"] = products
        else:
            products = rate["products"]
        if parameters is not None:
            args_have_changed = True
            rate["parameters"] = parameters
        else:
            parameters = rate["parameters"]
        if modifiers is not None:
            args_have_changed = True
            rate["modifiers"] = modifiers
        else:
            modifiers = rate["modifiers"]
        if reversible is not None:
            reversible_changed = True
            rate["reversible"] = reversible
        if dynamic_variables is not None:
            args_have_changed = True
            rate["dynamic_variables"] = dynamic_variables
        if args is not None:
            rate["dynamic_variables"] = [i for i in args if i in rate["dynamic_variables"]]
            rate["args"] = args
        else:
            if reversible_changed or args_have_changed:
                if dynamic_variables is None:
                    if rate["reversible"]:
                        dynamic_variables = substrates + products + modifiers
                    else:
                        dynamic_variables = substrates + modifiers
                    rate["dynamic_variables"] = dynamic_variables
                rate["args"] = dynamic_variables + parameters

        if dynamic_variables is None:
            dynamic_variables = rate["dynamic_variables"]

        self._check_for_existence(
            name=rate_name, check_against=self.get_all_compounds(), candidates=dynamic_variables
        )
        self._check_for_existence(
            name=rate_name, check_against=self.get_parameter_names(), candidates=parameters
        )

    def update_rates(self, rates: dict):
        for rate_name, rate in rates.items():
            self.update_rate(rate_name, **rate)

    def update_rate_meta_info(self, rate: str, meta_info: dict):
        """Update meta info of a rate.

        Parameters
        ----------
        rate : str
            Name of the rate
        meta_info : dict
            Meta info of the rate. Allowed keys are
            {common_name, gibbs0, ec, database_links, notes, sbml_function}
        """
        self.update_meta_info(component="rates", meta_info={rate: meta_info})

    def remove_rate(self, rate_name: str):
        """Remove a rate function from the model.

        Parameters
        ----------
        rate_name : str
            Name of the rate
        """
        del self.rates[rate_name]

    def remove_rates(self, rate_names: list[str]):
        """Remove multiple rate functions from the model.

        Parameters
        ----------
        rate_names : iterable(str)
            Names of the rates
        """
        for rate_name in rate_names:
            self.remove_rate(rate_name=rate_name)

    def get_rate_names(self) -> list[str]:
        """Return all rate names."""
        return list(self.rates)

    def get_rate_function(self, rate_name: str) -> callable:
        return self.rates[rate_name]["function"]

    def get_rate_parameters(self, rate_name: str) -> list[str]:
        """Get the parameters of a rate."""
        return list(self.rates[rate_name]["parameters"])

    def get_rate_substrates(self, rate_name: str) -> list[str]:
        """Get the substrates of a rate."""
        return list(self.rates[rate_name]["substrates"])

    def get_rate_products(self, rate_name) -> list[str]:
        """Get the products of a rate."""
        return list(self.rates[rate_name]["products"])

    def get_rate_modifiers(self, rate_name) -> list[str]:
        """Get the modifiers of a rate."""
        return list(self.rates[rate_name]["modifiers"])

    def get_rate_dynamic_variables(self, rate_name) -> list[str]:
        """Get the dynamic variables of a rate."""
        return list(self.rates[rate_name]["dynamic_variables"])

    def get_rate_args(self, rate_name) -> list[str]:
        """Get the rate function arguments of a rate."""
        return list(self.rates[rate_name]["args"])

    ##########################################################################
    # Simulation functions
    ##########################################################################

    def _get_fluxes(
        self,
        *,
        fcd: Union[dict[str, float], dict[str, list[float]]],
    ) -> Union[dict[str, float], dict[str, list[float]]]:
        # args = self.parameters | fcd # python 3.9+ syntax
        args = {**self.parameters, **fcd}
        fluxes = {}
        for name, rate in self.rates.items():
            try:
                fluxes[name] = rate["function"](*(args[arg] for arg in rate["args"]))
            except KeyError as e:
                raise KeyError(f"Could not find argument {e} for rate {name}")
        return fluxes

    ##########################################################################
    # Source code functions
    ##########################################################################

    def _generate_function_source_code(self) -> str:
        function_strings = []
        for name, function in self.functions.items():
            function_code = get_formatted_function_source_code(
                function_name=name, function=function, function_type="function"
            )
            function_strings.append(function_code)
        return "\n".join(sorted(function_strings))

    def _generate_rates_source_code(self, *, include_meta_info=True) -> tuple[str]:
        """Generate modelbase source code for rates.

        See Also
        --------
        generate_model_source_code
        """
        rate_functions = set()
        rates = []

        for name, rate in self.rates.items():
            function = rate["function"]
            substrates = rate["substrates"]
            products = rate["products"]
            modifiers = rate["modifiers"]
            parameters = rate["parameters"]
            reversible = rate["reversible"]
            args = rate["args"]

            function_code = get_formatted_function_source_code(
                function_name=name, function=function, function_type="rate"
            )
            rate_functions.add(function_code)
            rate_definition = (
                "m.add_rate(\n"
                f"    rate_name={repr(name)},\n"
                f"    function={function.__name__},\n"
                f"    substrates={substrates},\n"
                f"    products={products},\n"
                f"    modifiers={modifiers},\n"
                f"    parameters={parameters},\n"
                f"    reversible={reversible},\n"
                f"    args={args},\n"
            )
            if include_meta_info:
                meta_info = self._get_nonzero_meta_info(component="rates")
                try:
                    info = meta_info[name]
                    rate_definition += f"    **{info}\n"
                except KeyError:
                    pass
            rate_definition += ")"
            rates.append(rate_definition)
        return "\n".join(sorted(rate_functions)), "\n".join(rates)

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _create_sbml_rates(self, *, sbml_model: libsbml.Model):
        """Convert the rates into sbml reactions.

        Parameters
        ----------
        sbml_model : libsbml.Model
        """
        for rate_id, rate in self.rates.items():
            meta_info = self.meta_info["rates"][rate_id]

            rxn = sbml_model.createReaction()
            rxn.setId(convert_id_to_sbml(id_=rate_id, prefix="RXN"))
            name = meta_info.common_name
            if name:
                rxn.setName(name)
            rxn.setFast(False)
            rxn.setReversible(rate["reversible"])

            substrates = defaultdict(int)
            products = defaultdict(int)
            for compound in rate["substrates"]:
                substrates[compound] += 1
            for compound in rate["products"]:
                products[compound] += 1

            for compound, stoichiometry in substrates.items():
                sref = rxn.createReactant()
                sref.setSpecies(convert_id_to_sbml(id_=compound, prefix="CPD"))
                sref.setStoichiometry(stoichiometry)
                sref.setConstant(False)

            for compound, stoichiometry in products.items():
                sref = rxn.createProduct()
                sref.setSpecies(convert_id_to_sbml(id_=compound, prefix="CPD"))
                sref.setStoichiometry(stoichiometry)
                sref.setConstant(False)

            for compound in rate["modifiers"]:
                sref = rxn.createModifier()
                sref.setSpecies(convert_id_to_sbml(id_=compound, prefix="CPD"))

            function = meta_info.sbml_function
            if function is not None:
                kinetic_law = rxn.createKineticLaw()
                kinetic_law.setMath(libsbml.parseL3Formula(function))
