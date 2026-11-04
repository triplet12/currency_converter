import pytest
from converter.core import convert, UnknownCurrencyError
from converter.models import Rates
from datetime import datetime


time = datetime.now()
rate = Rates('USD', {'USD': 1,'RUB': 81, 'EUR': 0.15}, time, time)


def test_normal():
    assert convert(100, 'USD', 'RUB', rate) == 8100


def test_UnknownCurrencyError():
    with pytest.raises(UnknownCurrencyError, match="Валюта не найдена"):
        convert(100, 'USD', 'PYG', rate)


def test_neg_amount():
    with pytest.raises(ValueError):
            convert(-100, 'USD', 'PYG', rate)


def test_low_letters():
    assert convert(100, 'usd', 'RuB', rate) == 8100


def test_from_not_base_cur():
    assert convert(81000, 'RUB', 'EUR', rate) == 150

