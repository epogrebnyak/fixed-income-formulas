import pytest

from accumulation import Semiannual
from base import Float
from bond import Bond
from payments import Payment, Stream


def test_float():
    assert Float(1 / 3).round(2) == 0.33


def test_payments():
    x = Payment(1.21, t=2).present_value(interest_rate=0.1)
    assert round(x, 4) == 1


def test_stream():
    s = Stream.from_list([(-100, 0), (7, 0.5), (7, 1), (100, 1)])
    x = s.irr(Semiannual)
    assert round(x, 2) == 0.14


@pytest.fixture
def semibond():
    """Bond with 2 coupons per year."""
    return Bond(
        coupons_per_year=2,
        redemption=Payment(amount=100, t=1),
        coupons=[Payment(amount=7, t=0.5), Payment(amount=7, t=1)],
    )


def test_bond_ytm(semibond):
    assert semibond.ytm(price=100).round(4) == 0.1400


def test_bond_price(semibond):
    assert semibond.price(0.1400) == 100.0
