import pytest
from converter.api import parse_rates, ApiError
from converter.models import Rates
from datetime import datetime
from json import load
from pathlib import Path


def test_normal():
    with open(Path('data/usd.json')) as f:
        test_dict = load(f)
    lst_time = datetime.fromtimestamp(test_dict['time_last_update_unix'])
    nxt_time = datetime.fromtimestamp(test_dict['time_next_update_unix'])
    assert parse_rates(test_dict, 'USD') == Rates('USD', test_dict['rates'],lst_time, nxt_time)


def test_api_error():
    with pytest.raises(ApiError):
        assert parse_rates({"result": "error", "error-type": "test"}, 'USD')
