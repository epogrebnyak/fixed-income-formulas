from dataclasses import dataclass
from payments import Payment, Stream
from accumulation import Accumulation, Annual
from typing import Type 

@dataclass
class Bond:
  redemption: Payment
  coupons: list[Payment]
  accumulation: Type[Accumulation] = Annual

  @property
  def payments(self):
    return self.coupons + [self.redemption] 

  @property
  def stream(self):
    return Stream(self.payments)

  def price(self, interest_rate):
    return self.stream.npv(interest_rate, self.accumulation)

  def ytm(self, price):
    x = (price / 100) * self.redemption.amount # price is on par=100 basis
    s = Stream([Payment(x, 0)]+ self.payments)
    return s.irr()

  