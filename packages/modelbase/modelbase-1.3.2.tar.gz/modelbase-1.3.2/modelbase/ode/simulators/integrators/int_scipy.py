from __future__ import annotations

from typing import Union, Any

import numpy as np
import scipy.integrate as spi


class _IntegratorScipy:
    """Wrapper around scipy.odeint and scipy.ode."""

    def __init__(self, rhs: callable, y0: list[float]):
        self.rhs = rhs
        self.t0 = 0
        self.y0 = y0
        self.y0_orig = y0.copy()

    def get_integrator_kwargs(self):
        odeint_kwargs = {
            "ml": None,
            "mu": None,
            "rtol": 1e-8,  # manually set
            "atol": 1e-8,  # manually set
            "tcrit": None,
            "h0": 0.0,
            "hmax": 0.0,
            "hmin": 0.0,
            "ixpr": 0,
            "mxstep": 0,
            "mxhnil": 0,
            "mxordn": 12,
            "mxords": 5,
            "printmessg": 0,
            "tfirst": False,
        }
        ode_kwargs = {
            # internal ones
            "max_steps": 100000,
            "step_size": 1,
            # lsoda ones
            "first_step": None,
            "min_step": 0.0,
            "max_step": np.inf,
            "rtol": 1e-8,  # manually set
            "atol": 1e-8,  # manually set
            "jac": None,
            "lband": None,
            "uband": None,
        }
        return {"simulate": odeint_kwargs, "simulate_to_steady_state": ode_kwargs}

    def _simulate(
        self,
        *,
        t_end: float = None,
        steps: list[float] = None,
        time_points: list[float] = None,
        **integrator_kwargs,
    ) -> tuple[list[float], list[float]]:
        if time_points is not None:
            if time_points[0] != 0:
                t = [0]
                t.extend(time_points)
            else:
                t = time_points

        elif steps is not None:
            # Scipy counts the total amount of return points rather than
            # steps as assimulo
            steps += 1
            t = np.linspace(self.t0, t_end, steps)
        else:
            t = np.linspace(self.t0, t_end, 100)
        y = spi.odeint(func=self.rhs, y0=self.y0, t=t, tfirst=True, **integrator_kwargs)
        self.t0 = t[-1]
        self.y0 = y[-1, :]
        return t, y

    def _simulate_to_steady_state(
        self,
        *,
        tolerance: float,
        integrator_kwargs: dict[str, Any],
        simulation_kwargs: dict[str, Any],
    ) -> tuple[list[float], list[float]]:
        if "step_size" in simulation_kwargs:
            step_size = simulation_kwargs["step_size"]
        else:
            step_size = 1
        if "max_steps" in simulation_kwargs:
            max_steps = simulation_kwargs["max_steps"]
        else:
            max_steps = 100000
        if "integrator" in simulation_kwargs:
            integrator = simulation_kwargs["integrator"]
        else:
            integrator = "lsoda"
        self._reset()
        integ = spi.ode(self.rhs)
        integ.set_integrator(name=integrator, **integrator_kwargs)
        integ.set_initial_value(self.y0)
        t = self.t0 + step_size
        y0 = self.y0
        for step in range(max_steps):
            y = integ.integrate(t)
            if np.linalg.norm(y - y0, ord=2) < tolerance:
                return t, y
            else:
                y0 = y
                t += step_size
        raise ValueError("Could not find a steady state")

    def _reset(self):
        self.t0 = 0
        self.y0 = self.y0_orig.copy()
