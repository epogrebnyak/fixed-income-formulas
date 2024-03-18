# fixed-income-formulas
Interest rate and bond calculations in Python.

Course notebook: https://colab.research.google.com/drive/1e0EeOFs0EzKYtwGBzHGFwgf6JocFkL4r

```python
from bond import Bond
from payments import Payment

b = Bond(
    coupons_per_year=2,
    redemption=Payment(amount=100, t=1),
    coupons=[Payment(amount=7, t=0.5), Payment(amount=7, t=1)],
)

b.ytm(price=100).round(4)  # 0.1400
b.price(0.1400)  # 100.0
```

Next:
- [ ] plot_stream 
- [ ] make_bond
- [ ] shift steam or bond in time
