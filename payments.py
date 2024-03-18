"""Streams of payments and their present value and IRR/YTM calculations."""

from dataclasses import dataclass, field

from scipy.optimize import newton

from accumulation import Annual
from base import Float


@dataclass
class Payment:
    """Represent payment of *amount* value at specific point of time *t* in the future.

    Parameters
    ----------

      amount: float
       Money amount in currency units.

      t: float
       Time in years.

    """

    amount: float
    t: float

    def present_value(self, interest_rate, accumulation=Annual) -> float:
        """Return present value using annual or some other type of interest rate for discounting."""
        return self.amount / accumulation(interest_rate).fv(self.t)


@dataclass
class Stream:
    payments: list[Payment] = field(default_factory=list)

    @classmethod
    def from_list(cls, xs):
        return cls([Payment(*x) for x in xs])

    def add(self, amount, t):
        p = Payment(amount, t)
        self.payments.append(p)
        return self

    def sort(self) -> "Stream":
        """Sort payments by timestamp."""
        self.payments = sorted(self.payments, key=lambda x: (x.t, x.amount))
        return self

    def npv(self, interest_rate: float, accumulation=Annual) -> float:
        return sum(
            [p.present_value(interest_rate, accumulation) for p in self.payments]
        )

    def irr(self, accumulation=Annual) -> float:
        values = [p.amount for p in self.payments]
        timestamps = [p.t for p in self.payments]
        return irr(values, timestamps, accumulation)


def discounted_values(discount_with, cashflows, timestamps):
    return [x / discount_with.fv(t) for x, t in zip(cashflows, timestamps)]


def npv(interest_rate, cashflows, timestamps=None, accumulation=Annual) -> Float:
    if timestamps is None:
        timestamps = list(range(len(cashflows)))
    discount_with = accumulation(interest_rate)
    return Float(sum(discounted_values(discount_with, cashflows, timestamps)))


def irr(cashflows, timestamps, accumulation) -> Float:
    def f(interest_rate):
        return npv(interest_rate, cashflows, timestamps, accumulation)

    return Float(newton(f, x0=0.1))


def annuity(
    amount: float, periods_per_year: int, years: int, months: int = 0
) -> list[Payment]:
    n_years = (years * 12 + months) / 12
    return [Payment(amount, t) for t in sequence(n_years, periods_per_year)]


def sequence(n_years: int, periods_per_year: int):
    step = 1 / periods_per_year
    return list((x + 1) * step for x in range(n_years * periods_per_year))
