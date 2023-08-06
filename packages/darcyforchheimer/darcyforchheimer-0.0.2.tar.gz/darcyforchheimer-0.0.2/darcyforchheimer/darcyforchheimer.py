import numpy as np
from scipy.optimize import curve_fit


def fit_func(x, b, c):
    """
    Forces the curve fitting to go thru 0,0
    """
    return b * x ** 2 + c * x


def calculate_coefficients(
    velocity: list, pressure: list, thickness, density, viscosity, absolute=False
):
    """
    Returns the D and F coeeficients, normalized per thickness
    velocity [m/s]
    pressure [Pa]
    thickness [m]
    density [kg/m3]
    viscosity [Pa*s]
    """
    norm_pressure = [p / thickness if not absolute else p for p in pressure]
    params = curve_fit(fit_func, velocity, norm_pressure)
    [f, r] = params[0]
    vel_fit = np.linspace(velocity[0], velocity[-1], 500)
    p_fit = f * vel_fit ** 2 + r * vel_fit
    F = 2 * f / density
    D = r / viscosity
    return (D, F)
