from bond import Bond
from payments import Payment

b = Bond(
    coupons_per_year=2,
    redemption=Payment(amount=100, t=1),
    coupons=[Payment(amount=7, t=0.5), Payment(amount=7, t=1)],
)

print(b.ytm(price=100).round(4))  # 0.1400
print(b.price(0.1400))  # 100.0


b2 = make_bond(coupon_rate=0.14, coupons_per_year=2, years=1)
