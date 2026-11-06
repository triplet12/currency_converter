from converter.models import Rates
from datetime import datetime, timedelta

def test_not_exprd():
    now = datetime.now()
    rate = Rates('USD', {}, now - timedelta(1), now + timedelta(1))
    assert rate.is_expired(now) == False


def test_exprd():
    some_date = datetime(2026, 5, 5)
    before_some_date = datetime(2026, 3, 5) 
    after_some_date = datetime(2026, 7, 5) 
    rate = Rates('USD', {}, before_some_date, some_date)
    assert rate.is_expired(after_some_date) == True


def test_equal_exprd():
    some_date = datetime(2026, 5, 5)
    before_some_date = datetime(2026, 3, 5) 
    rate = Rates('USD', {}, before_some_date, some_date)
    assert rate.is_expired(some_date) == True