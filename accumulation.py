"""Interest rate calcualtions."""

from abc import ABC
from dataclasses import dataclass

import numpy as np


def simple(interest_rate, t):
    return 1 + t * interest_rate


def compound(interest_rate, t, frequency):
    return (1 + interest_rate / frequency) ** (t * frequency)


def continious(interest_rate, t):
    return np.exp(interest_rate * t)


def annual(interest_rate, t):
    return compound(interest_rate, t, frequency=1)


def semiannual(interest_rate, t):
    return compound(interest_rate, t, frequency=2)


def quarterly(interest_rate, t):
    return compound(interest_rate, t, frequency=4)


def monthly(interest_rate, t):
    return compound(interest_rate, t, frequency=12)


accumulation_functions = [simple, continious, annual, semiannual, quarterly, monthly]


@dataclass
class Accumulation(ABC):
    interest_rate: float

    def fv(self, t): ...

    @staticmethod
    def from_frequency(m_periods_per_year):
        return {1: Annual, 2: Semiannual, 4: Quarterly, 12: Monthly}[m_periods_per_year]


class Annual(Accumulation):
    def fv(self, t):
        return annual(self.interest_rate, t)


class Semiannual(Accumulation):
    def fv(self, t):
        return semiannual(self.interest_rate, t)


class Quarterly(Accumulation):
    def fv(self, t):
        return quarterly(self.interest_rate, t)


class Monthly(Accumulation):
    def fv(self, t):
        return monthly(self.interest_rate, t)


class Continious(Accumulation):
    def fv(self, t):
        return continious(self.interest_rate, t)
