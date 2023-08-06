from __future__ import annotations

from typing import Union, Any, Callable
import numpy as np

# This warning comes from assimulo
np.warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

from assimulo.problem import Explicit_Problem
from assimulo.solvers import CVode
from assimulo.solvers.sundials import CVodeError


class _IntegratorAssimulo:
    """Wrap around assimulo CVODE."""

    def __init__(self, rhs: Callable, y0: list[float]):
        self.problem = Explicit_Problem(rhs, y0)
        self.integrator = CVode(self.problem)
        self._integrator_kwargs = [
            "atol",
            "backward",
            "clock_step",
            "discr",
            "display_progress",
            "dqrhomax",
            "dqtype",
            "external_event_detection",
            "inith",
            "linear_solver",
            "maxcor",
            "maxcorS",
            "maxh",
            "maxkrylov",
            "maxncf",
            "maxnef",
            "maxord",
            "maxsteps",
            "minh",
            "norm",
            "num_threads",
            "pbar",
            "precond",
            "report_continuously",
            "rtol",
            "sensmethod",
            "suppress_sens",
            "time_limit",
            "usejac",
            "usesens",
            "verbosity",
        ]

    def get_integrator_kwargs(self) -> dict[str, Any]:
        return {k: getattr(self.integrator, k) for k in self._integrator_kwargs}

    def _simulate(
        self,
        *,
        t_end: float = None,
        steps: list[float] = None,
        time_points: list[float] = None,
        **integrator_kwargs,
    ) -> tuple[list[float], list[float]]:
        if steps is None:
            steps = 0
        for k, v in integrator_kwargs.items():
            setattr(self.integrator, k, v)
        return self.integrator.simulate(t_end, steps, time_points)

    def _simulate_to_steady_state(
        self,
        *,
        tolerance: float,
        integrator_kwargs: dict[str, Any],
        simulation_kwargs: dict[str, Any],
    ) -> tuple[list[float], list[float]]:
        for k, v in integrator_kwargs.items():
            setattr(self.integrator, k, v)
        if "max_rounds" in simulation_kwargs:
            max_rounds = simulation_kwargs["max_rounds"]
        else:
            max_rounds = 3
        self._reset()
        t_end = 1000
        for n_round in range(1, max_rounds + 1):
            try:
                t, y = self.integrator.simulate(t_end)
                if np.linalg.norm(y[-1] - y[-2], ord=2) < tolerance:
                    return t[-1], y[-1]
                else:
                    t_end *= 1000
            except CVodeError:
                raise ValueError("Could not find a steady state")
        raise ValueError("Could not find a steady state")

    def _reset(self):
        """Reset the integrator."""
        self.integrator.reset()
