import numpy as np
from dataclasses import dataclass


@dataclass
class Params:
    mass: float = 100
    mu: float = 398600.4415e9
    R: float = 6371e3
    e0: float = 4.2666e-6


def calc_force(t, q, params):
    r = q[0:3]
    radius = np.linalg.norm(r)
    return -(params.mu * params.mass / radius ** 3) * r


def calc_f(t, q, params):
    acc = calc_force(t, q, params) / params.mass

    return np.array([
        q[3],
        q[4],
        q[5],

        acc[0],
        acc[1],
        acc[2]
    ])


def make_iter_runge_kutta(t, q, params, h):
    k1 = calc_f(t, q, params)

    k2 = calc_f(t + h / 2, q + (h / 2) * k1, params)
    k3 = calc_f(t + h / 2, q + (h / 2) * k2, params)
    k4 = calc_f(t + h, q + h * k3, params)
    return q + (h / 6) * (k1 + 2 * (k2 + k3) + k4)


