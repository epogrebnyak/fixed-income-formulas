from accumulation import Semiannual
from payments import Payment, Stream
from bond import Bond 

def test_payments():
    x = Payment(1.21, t=2).present_value(interest_rate=0.1)
    assert round(x, 4) == 1


def test_stream():
    s = Stream.from_list([(-100, 0), (7, 0.5), (7, 1), (100, 1)])
    x = s.irr(Semiannual)
    assert round(x, 2) == 0.14

def test_bond():
    b = Bond(redemption=Payment(100, 1),
             coupons=[Payment(7, .5), 
                      Payment(7, 1)],
             accumulation=Semiannual)
    assert b.ytm(100) == 0.1449
    assert b.price(0.1449) == 100.0    
