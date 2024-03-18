"""Bond represented as stream of payments."""

from dataclasses import dataclass
from typing import Type

from accumulation import Accumulation
from payments import Payment, Stream, annuity


@dataclass
class Bond:
    coupons_per_year: int  # 1, 2, 4 or 12 (typically - 2)
    redemption: (
        Payment  # principal payment at the end of period for all bonds, no amortisation
    )
    coupons: list[Payment]

    @property
    def accumulation(self) -> Type[Accumulation]:
        """Select default discount factor based on number of coupons per year."""
        return Accumulation.from_frequency(self.coupons_per_year)

    @property
    def payments(self):
        """All cashflows associated with a bond, coupons and principal."""
        return self.coupons + [self.redemption]

    @property
    def stream(self):
        """Cashflows associated with a bond as a `Stream` instance."""
        return Stream(self.payments)

    def price(self, interest_rate, accumulation=None):
        """Calculate price of a bond given an interest rate."""
        if not accumulation:
            accumulation = self.accumulation
        return self.stream.npv(interest_rate, self.accumulation)

    def ytm(self, price, accumulation=None):
        """Calculate yiled to maturity (YTM) of a bond given price of bond.
        The price should be expressed on par = 100 basis (eg 102.3, 98.5 and so on).
        """
        x = (price / 100) * self.redemption.amount
        if not accumulation:
            accumulation = self.accumulation
        return Stream([Payment(-x, 0)] + self.payments).irr(accumulation)


def make_bond(
    coupon_rate: float, coupons_per_year: int, years: int, months: int, par: int = 100
) -> Bond:
    coupon = par * coupon_rate / coupons_per_year
    coupons = annuity(coupon, coupons_per_year, years, months)
    redemption = Payment(par, (years * 12 + months) / 12)
    return Bond(coupons_per_year, redemption, coupons)
