import pytest
from converter.core import convert, UnknownCurrencyError
from converter.models import Rates
from datetime import datetime


time = datetime.now()
rate = Rates('USD', {'USD': 1,'RUB': 81}, time, time)


def test_normal():
    assert convert(100, 'USD', 'RUB', rate) == 8100


def test_UnknownCurrencyError():
    with pytest.raises(UnknownCurrencyError, match="Валюта не найдена"):
        convert(100, 'USD', 'PYG', rate)


def test_neg_amount():
    with pytest.raises(ValueError):
            convert(-100, 'USD', 'PYG', rate)