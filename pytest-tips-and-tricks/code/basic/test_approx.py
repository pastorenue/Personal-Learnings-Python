import pytest
from rpncalc.utils import calc


def test_add():
    res = calc(0.2, 0.1, "+")
    assert res == pytest.approx(0.3)

def test_another_add():
    res = calc(0.2, 0.1, "+")
    assert res == 0.6
