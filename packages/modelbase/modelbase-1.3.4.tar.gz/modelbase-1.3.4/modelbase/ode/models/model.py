"""Main ODE model module.

Description of the module
"""
from __future__ import annotations

import subprocess
import warnings
from typing import Union, Iterable, Callable

import libsbml
import numpy as np
import pandas as pd

from ...core import (
    AlgebraicMixin,
    BaseModel,
    CompoundMixin,
    ParameterMixin,
    RateMixin,
    StoichiometricMixin,
)
from ...core.utils import convert_id_to_sbml


class Model(
    RateMixin,
    StoichiometricMixin,
    AlgebraicMixin,
    ParameterMixin,
    CompoundMixin,
    BaseModel,
):
    """The main class for modeling. Provides model construction and inspection tools."""

    def __init__(
        self,
        parameters: dict = None,
        compounds: dict = None,
        algebraic_modules: dict = None,
        rate_stoichiometries: dict = None,
        rates: dict = None,
        functions: dict = None,
        meta_info: dict = None,
    ):
        BaseModel.__init__(self, meta_info=meta_info)
        CompoundMixin.__init__(self, compounds=compounds)
        ParameterMixin.__init__(self, parameters=parameters)
        AlgebraicMixin.__init__(self, algebraic_modules=algebraic_modules)
        StoichiometricMixin.__init__(self, rate_stoichiometries=rate_stoichiometries)
        RateMixin.__init__(self, rates=rates, functions=functions)
        self.meta_info["model"].sbo = "SBO:0000062"  # continuous framework

    def __str__(self):
        """Give a string representation.

        Returns
        -------
        representation : str
        """
        return (
            "Model:"
            + f"\n    {len(self.get_compounds())} Compounds"
            + f"\n    {len(self.get_stoichiometries())} Reactions"
        )

    def _element_difference(self, other: Model, attribute: str):
        self_collection = getattr(self, attribute)
        other_collection = getattr(other, attribute)
        difference = sorted(set(other_collection).difference(self_collection))
        if not difference:
            return None
        if attribute == "compounds":
            return difference
        return {k: other_collection[k] for k in difference}

    def _element_intersection(self, other: Model, attribute: str):
        self_collection = getattr(self, attribute)
        other_collection = getattr(other, attribute)
        intersection: list[str] = sorted(set(self_collection).intersection(other_collection))
        if not intersection:
            return None
        if attribute == "compounds":
            return intersection
        return {k: other_collection[k] for k in intersection}

    def __add__(self, other: Model) -> Model:
        m = self.copy()
        m.add(**{"compounds": self._element_difference(other, "compounds")})

        for name, module in other.algebraic_modules.items():
            if name in self.algebraic_modules:
                m.update_algebraic_module(name, **module)
            else:
                m.add_algebraic_module(name, **module)

        for attribute in [
            "parameters",
            "rates",
            "stoichiometries",
            "functions",
        ]:
            m.add(**{attribute: self._element_difference(other, attribute)})
            m.update(**{attribute: self._element_intersection(other, attribute)})
        return m

    def __iadd__(self, other: Model) -> Model:
        self.add(**{"compounds": self._element_difference(other, "compounds")})
        for name, module in other.algebraic_modules.items():
            if name in self.algebraic_modules:
                self.update_algebraic_module(name, **module)
            else:
                self.add_algebraic_module(name, **module)

        for attribute in [
            "parameters",
            "rates",
            "stoichiometries",
            "functions",
        ]:
            self.add(**{attribute: self._element_difference(other, attribute)})
            self.update(**{attribute: self._element_intersection(other, attribute)})
        return self

    def __sub__(self, other: Model) -> Model:
        m = self.copy()
        for attribute in [
            "compounds",
            "parameters",
            "algebraic_modules",
            "rates",
            "stoichiometries",
            "functions",
        ]:
            m.remove(**{attribute: self._element_intersection(other, attribute)})
        return m

    def __isub__(self, other: Model) -> Model:
        for attribute in [
            "compounds",
            "parameters",
            "algebraic_modules",
            "rates",
            "stoichiometries",
            "functions",
        ]:
            self.remove(**{attribute: self._element_intersection(other, attribute)})
        return self

    def add(
        self,
        compounds: list = None,
        parameters: dict[str, float] = None,
        algebraic_modules: dict[str, dict] = None,
        rates: dict[str, dict] = None,
        stoichiometries: dict[str, dict] = None,
        functions: dict[str, callable] = None,
    ):
        if compounds is not None:
            self.add_compounds(compounds)
        if parameters is not None:
            self.add_parameters(parameters)
        if algebraic_modules is not None:
            self.add_algebraic_modules(algebraic_modules)
        if rates is not None:
            self.add_rates(rates)
        if stoichiometries is not None:
            self.add_stoichiometries(stoichiometries)
        if functions is not None:
            self.add_functions(functions)

    def update(
        self,
        parameters: dict[str, float] = None,
        algebraic_modules: dict[str, dict] = None,
        rates: dict[str, dict] = None,
        stoichiometries: dict[str, dict] = None,
        functions: dict[str, callable] = None,
    ):
        if parameters is not None:
            self.update_parameters(parameters)
        if algebraic_modules is not None:
            self.update_algebraic_modules(algebraic_modules)
        if rates is not None:
            self.update_rates(rates)
        if stoichiometries is not None:
            self.update_stoichiometries(stoichiometries)
        if functions is not None:
            self.update_functions(functions)

    def remove(
        self,
        compounds: list[str] = None,
        parameters: list[str] = None,
        algebraic_modules: list[str] = None,
        rates: list[str] = None,
        stoichiometries: list[str] = None,
        functions: list[str] = None,
    ):
        if compounds is not None:
            self.remove_compounds(compounds)
        if parameters is not None:
            self.remove_parameters(parameters)
        if algebraic_modules is not None:
            self.remove_algebraic_modules(algebraic_modules)
        if rates is not None:
            self.remove_rates(rates)
        if stoichiometries is not None:
            self.remove_rate_stoichiometries(stoichiometries)
        if functions is not None:
            self.remove_functions(functions)

    ##########################################################################
    # Reactions
    ##########################################################################

    def add_reaction(
        self,
        rate_name: str,
        function: Callable,
        stoichiometry: dict[str, int],
        modifiers: list[str] = None,
        parameters: list[str] = None,
        dynamic_variables: list[str] = None,
        args: list[str] = None,
        reversible: bool = False,
        check_consistency: bool = True,
        **meta_info,
    ):
        """Add a reaction to the model.

        Shortcut for add_rate and add stoichiometry functions.

        See Also
        --------
        add_rate
        add_stoichiometry

        Examples
        --------
        >>> add_reaction(
        >>>     rate_name="v1",
        >>>     function=mass_action,
        >>>     stoichiometry={"X": -1, "Y": 1},
        >>>     parameters=["k2"],
        >>> )

        >>> add_reaction(
        >>>     rate_name="v1",
        >>>     function=reversible_mass_action,
        >>>     stoichiometry={"X": -1, "Y": 1},
        >>>     parameters=["k1_fwd", "k1_bwd"],
        >>>     reversible=True,
        >>> )
        """
        substrates = [k for k, v in stoichiometry.items() if v < 0]
        products = [k for k, v in stoichiometry.items() if v > 0]

        self.add_rate(
            rate_name=rate_name,
            function=function,
            substrates=substrates,
            products=products,
            dynamic_variables=dynamic_variables,
            modifiers=modifiers,
            parameters=parameters,
            reversible=reversible,
            args=args,
            check_consistency=check_consistency,
            **meta_info,
        )
        self.add_stoichiometry(rate_name=rate_name, stoichiometry=stoichiometry)

    def update_reaction(
        self,
        rate_name: str,
        function: Callable = None,
        stoichiometry: dict[str, float] = None,
        modifiers: list[str] = None,
        parameters: list[str] = None,
        dynamic_variables: list[str] = None,
        args: list[str] = None,
        reversible: bool = None,
        check_consistency: bool = True,
    ):
        """Update an existing reaction.

        Parameters
        ----------
        rate_name : str
        function : Callable, optional
        stoichiometry : dict, optional
        modifiers: iterable(str), optional
        parameters: iterable(str), optional
        reversible: bool, optional

        See Also
        --------
        add_reaction
        update_rate
        update_stoichiometry
        """
        if stoichiometry is not None:
            substrates = [k for k, v in stoichiometry.items() if v < 0]
            products = [k for k, v in stoichiometry.items() if v > 0]
        else:
            substrates = None
            products = None
        self.update_rate(
            rate_name=rate_name,
            function=function,
            substrates=substrates,
            products=products,
            modifiers=modifiers,
            parameters=parameters,
            reversible=reversible,
            dynamic_variables=dynamic_variables,
            args=args,
            check_consistency=check_consistency,
        )
        if stoichiometry is not None:
            self.update_stoichiometry(rate_name=rate_name, stoichiometry=stoichiometry)

    def update_reactions(self, reactions: dict):
        for rate_name, reaction in reactions.items():
            self.update_reaction(rate_name, **reaction)

    def add_reaction_from_ratelaw(
        self,
        rate_name: str,
        ratelaw: "modelbase.ode.utils.ratelaw.BaseRateLaw",
        **meta_info,
    ):
        """Add a reaction from a ratelaw.

        Parameters
        ----------
        rate_name
        ratelaw : modelbase.ode.utils.ratelaw.BaseRateLaw
            Ratelaw instance
        meta_info

        Examples
        --------
        >>> add_reaction_from_ratelaw(
                rate_name="v1",
                ratelaw=ReversibleMassAction(
                    substrates=["X"],
                    products=["Y"],
                    k_fwd="k1p",
                    k_bwd="k1m"
                ),
            )
        """
        default_meta_info = {"sbml_function": ratelaw.get_sbml_function_string()}
        default_meta_info.update(meta_info)

        self.add_rate(
            rate_name=rate_name,
            function=ratelaw.get_rate_function(),
            substrates=ratelaw.substrates,
            products=ratelaw.products,
            modifiers=ratelaw.modifiers,
            parameters=ratelaw.parameters,
            reversible=ratelaw.reversible,
            **default_meta_info,
        )
        self.add_stoichiometry(rate_name=rate_name, stoichiometry=ratelaw.stoichiometry)

    def remove_reaction(self, rate_name: str):
        """Remove a reaction from the model.

        Parameters
        ----------
        rate_name : str
        """
        self.remove_rate(rate_name=rate_name)
        self.remove_rate_stoichiometry(rate_name=rate_name)

    def remove_reactions(self, rate_names: list[str]):
        """Remove multiple reactions from the model.

        Parameters
        ----------
        names : iterable(str)
        """
        for rate_name in rate_names:
            self.remove_reaction(rate_name=rate_name)

    ##########################################################################
    # Simulation functions
    ##########################################################################

    def get_full_concentration_dict(
        self,
        y: Union[dict[str, float], dict[str, list[float]], np.ndarray[float], list[float]],
        t: float = 0.0,
    ) -> dict[str, np.ndarray]:
        """Calculate the derived variables (at time(s) t).

        Examples
        --------
        >>> get_full_concentration_dict(y=[0, 0])
        >>> get_full_concentration_dict(y={"X": 0, "Y": 0})
        """
        self._update_derived_parameters()
        if isinstance(t, (int, float)):
            t = [t]
        t = np.array(t)
        if isinstance(y, dict):
            y = {k: np.ones(len(t)) * v for k, v in y.items()}
        else:
            y = dict(zip(self.get_compounds(), (np.ones((len(t), 1)) * y).T))
        return {k: np.ones(len(t)) * v for k, v in self._get_fcd(t=t, y=y).items()}

    def get_fluxes_dict(
        self,
        y: Union[dict[str, float], dict[str, list[float]], np.ndarray[float], list[float]],
        t: float = 0.0,
    ) -> dict[str, np.ndarray]:
        """Calculate the fluxes at time point(s) t."""
        self._update_derived_parameters()
        fcd = self.get_full_concentration_dict(y=y, t=t)
        return {k: np.ones(len(fcd["time"])) * v for k, v in self._get_fluxes(fcd=fcd).items()}

    def get_fluxes_array(
        self,
        y: Union[dict[str, float], dict[str, list[float]], np.ndarray[float], list[float]],
        t: float = 0.0,
    ) -> np.ndarray:
        """Calculate the fluxes at time point(s) t."""
        return np.array([i for i in self.get_fluxes_dict(y=y, t=t).values()]).T

    def get_fluxes_df(
        self,
        y: Union[dict[str, float], dict[str, list[float]], np.ndarray[float], list[float]],
        t: float = 0.0,
    ) -> pd.DataFrame:
        """Calculate the fluxes at time point(s) t."""
        if isinstance(t, (int, float)):
            t = [t]
        return pd.DataFrame(data=self.get_fluxes_dict(y=y, t=t), index=t, columns=self.get_rate_names())

    # This can't get keyword-only arguments, as the integrators are calling it with
    # positional arguments
    def _get_rhs(self, t: float, y: list[float]) -> np.ndarray:
        """Calculate the right hand side of the ODE system.

        This is the more performant version of get_right_hand_side()
        and thus returns only an array instead of a dictionary.

        Watch out that this function swaps t and y!
        """
        y = dict(zip(self.get_compounds(), np.array(y).reshape(-1, 1)))
        fcd = self._get_fcd(t=t, y=y)
        fluxes = self._get_fluxes(fcd=fcd)
        compounds_local = self.get_compounds()
        dxdt = dict(zip(compounds_local, np.zeros(len(compounds_local))))
        for k, stoc in self.stoichiometries_by_compounds.items():
            for flux, n in stoc.items():
                dxdt[k] += n * fluxes[flux]
        return np.array([dxdt[i] for i in compounds_local]).flatten()

    def get_right_hand_side(
        self,
        y: Union[dict[str, float], dict[str, list[float]], np.ndarray[float], list[float]],
        t: float = 0.0,
    ) -> dict[str, float]:
        """Calculate the right hand side of the ODE system."""
        self._update_derived_parameters()
        y = self.get_full_concentration_dict(y=y, t=t)
        y = [y[i] for i in self.get_compounds()]
        rhs = self._get_rhs(t=t, y=y)
        eqs = [f"d{cpd}dt" for cpd in self.get_compounds()]
        return dict(zip(eqs, rhs))

    ##########################################################################
    # Model conversion functions
    ##########################################################################

    def to_labelmodel(
        self, labelcompounds: dict[str, int], labelmaps: dict[str, list[int]]
    ) -> "modelbase.ode.LabelModel":
        """Create a LabelModel from this model.

        Examples
        --------
        >>> m = Model()
        >>> m.add_reaction(
                rate_name="TPI",
                function=reversible_mass_action_1_1,
                stoichiometry={"GAP": -1, "DHAP": 1},
                parameters=["kf_TPI", "kr_TPI"],
                reversible=True,
            )
        >>> labelcompounds = {"GAP": 3, "DHAP": 3}
        >>> labelmaps = {"TPI": [2, 1, 0]}
        >>> m.to_labelmodel(labelcompounds=labelcompounds, labelmaps=labelmaps)
        """

        from modelbase.ode import LabelModel

        lm = LabelModel()
        lm.add_parameters(self.parameters)
        for compound in self.get_compounds():
            if compound in labelcompounds:
                lm.add_label_compound(compound=compound, num_labels=labelcompounds[compound])
            else:
                lm.add_compound(compound=compound)

        for module_name, module in self.algebraic_modules.items():
            lm.add_algebraic_module(
                module_name=module_name,
                function=module["function"],
                compounds=module["compounds"],
                derived_compounds=module["derived_compounds"],
                modifiers=module["modifiers"],
                parameters=module["parameters"],
            )

        for rate_name, rate_dict in self.rates.items():
            if rate_name not in labelmaps:
                lm.add_reaction(
                    rate_name=rate_name,
                    function=rate_dict["function"],
                    stoichiometry=self.stoichiometries[rate_name],
                    modifiers=rate_dict["modifiers"],
                    parameters=rate_dict["parameters"],
                    reversible=rate_dict["reversible"],
                )
            else:
                lm.add_labelmap_reaction(
                    rate_name=rate_name,
                    function=rate_dict["function"],
                    stoichiometry=self.stoichiometries[rate_name],
                    labelmap=labelmaps[rate_name],
                    modifiers=rate_dict["modifiers"],
                    parameters=rate_dict["parameters"],
                    reversible=rate_dict["reversible"],
                )
        return lm

    def to_linear_labelmodel(
        self, labelcompounds: dict[str, int], labelmaps: dict[str, list[int]]
    ) -> "modelbase.ode.LinearLabelModel":
        """Create a LinearLabelModel from this model.

        Watch out that for a linear label model reversible reactions have to be split
        into a forward and backward part.

        Examples
        --------
        >>> m = Model()
        >>> m.add_reaction(
        >>>     rate_name="TPI_fwd",
        >>>     function=_mass_action_1_1,
        >>>     stoichiometry={"GAP": -1, "DHAP": 1},
        >>>     parameters=["kf_TPI"],
        >>> )
        >>> m.add_reaction(
        >>>     rate_name="TPI_bwd",
        >>>     function=mass_action_1_1,
        >>>     stoichiometry={"DHAP": -1, "GAP": 1},
        >>>     parameters=["kr_TPI"],
        >>> )
        >>> labelcompounds = {"GAP": 3, "DHAP": 3}
        >>> labelmaps = {"TPI_fwd": [2, 1, 0], 'TPI_bwd': [2, 1, 0]}
        >>> m.to_linear_labelmodel(labelcompounds=labelcompounds, labelmaps=labelmaps)
        """

        from modelbase.ode import LinearLabelModel

        lm = LinearLabelModel()
        for compound in self.get_compounds():
            if compound in labelcompounds:
                lm.add_compound(compound=compound, num_labels=labelcompounds[compound])

        for rate_name, rate_dict in self.rates.items():
            if rate_name in labelmaps:
                if rate_dict["reversible"]:
                    warnings.warn(
                        f"Reaction {rate_name} is annotated as reversible. "
                        "Did you remember to split it into a forward and backward part?"
                    )
                lm.add_reaction(
                    rate_name=rate_name,
                    stoichiometry={
                        k: v for k, v in self.stoichiometries[rate_name].items() if k in labelcompounds
                    },
                    labelmap=labelmaps[rate_name],
                )
            else:
                warnings.warn(f"Skipping reaction {rate_name} as no labelmap is given")
        return lm

    ##########################################################################
    # Source code functions
    ##########################################################################

    def generate_model_source_code(self, linted: bool = True, include_meta_info: bool = False) -> str:
        """Generate source code of the model.

        Parameters
        ----------
        linted
            Whether the source code should be formatted via black.
            Usually it only makes sense to turn this off if there is an error somewhere.
        include_meta_info
            Whether to include meta info of the model components
        """
        parameters = self._generate_parameters_source_code(include_meta_info=include_meta_info)
        compounds = self._generate_compounds_source_code(include_meta_info=include_meta_info)
        functions = self._generate_function_source_code()
        module_functions, modules = self._generate_algebraic_modules_source_code(
            include_meta_info=include_meta_info
        )
        rate_functions, rates = self._generate_rates_source_code(include_meta_info=include_meta_info)
        stoichiometries = self._generate_stoichiometries_source_code()

        model_string = "\n".join(
            (
                "import math",
                "import numpy as np",
                "from modelbase.ode import Model, Simulator",
                functions,
                module_functions,
                rate_functions,
                "m = Model()",
                parameters,
                compounds,
                modules,
                rates,
                stoichiometries,
            )
        )
        if linted:
            blacked_string = subprocess.run(["black", "-c", model_string], stdout=subprocess.PIPE)
            return blacked_string.stdout.decode("utf-8")
        else:
            return model_string

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _create_sbml_reactions(self, *, sbml_model: libsbml.Model):
        """Create the reactions for the sbml model."""
        for rate_id, stoichiometry in self.stoichiometries.items():
            rate = self.meta_info["rates"][rate_id]
            rxn = sbml_model.createReaction()
            rxn.setId(convert_id_to_sbml(id_=rate_id, prefix="RXN"))
            name = rate.common_name
            if name:
                rxn.setName(name)
            rxn.setFast(False)
            rxn.setReversible(self.rates[rate_id]["reversible"])

            for compound_id, factor in stoichiometry.items():
                if factor < 0:
                    sref = rxn.createReactant()
                else:
                    sref = rxn.createProduct()
                sref.setSpecies(convert_id_to_sbml(id_=compound_id, prefix="CPD"))
                sref.setStoichiometry(abs(factor))
                sref.setConstant(False)

            for compound in self.rates[rate_id]["modifiers"]:
                sref = rxn.createModifier()
                sref.setSpecies(convert_id_to_sbml(id_=compound, prefix="CPD"))

            function = rate.sbml_function
            if function is not None:
                kinetic_law = rxn.createKineticLaw()
                kinetic_law.setMath(libsbml.parseL3Formula(function))

    def _model_to_sbml(self) -> libsbml.SBMLDocument:
        """Export model to sbml."""
        doc = self._create_sbml_document()
        sbml_model = self._create_sbml_model(doc=doc)
        self._create_sbml_units(sbml_model=sbml_model)
        self._create_sbml_compartments(sbml_model=sbml_model)
        self._create_sbml_compounds(sbml_model=sbml_model)
        if bool(self.algebraic_modules):
            self._create_sbml_algebraic_modules(sbml_model=sbml_model)
        self._create_sbml_reactions(sbml_model=sbml_model)
        return doc
