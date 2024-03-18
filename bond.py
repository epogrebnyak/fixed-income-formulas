"""Bond represented as stream of payments."""

from dataclasses import dataclass
from typing import Type

from accumulation import Accumulation, select_accumulation
from payments import Payment, Stream


@dataclass
class Bond:
    coupons_per_year: int # 1, 2, 4, typically 2
    redemption: Payment # principal payment at the end of period for all bonds, no amortisation
    coupons: list[Payment]

    @property
    def accumulation(self) -> Type[Accumulation]:
        """Default discount factor based on number of coupons per year."""
        return select_accumulation(self.coupons_per_year)

    @property
    def payments(self):
        """Cashflows associated with a bond."""        
        return self.coupons + [self.redemption]

    @property
    def stream(self):
        """Cashflows associated with a bond (as a `Stream` instance)."""        
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
        # accept price on par=100 basis
        x = (price / 100) * self.redemption.amount
        if not accumulation:
            accumulation = self.accumulation
        return Stream([Payment(-x, 0)] + self.payments).irr(accumulation)
