import requests
from .models import Rates
from datetime import datetime
from decorators_kit import retry


class ApiError(Exception):
    pass


def parse_rates(data: dict, base: str) -> Rates:         # словарь из JSON → Rates; без сети
    last_upd_time = datetime.fromtimestamp(data['time_last_update_unix'])
    next_upd_time = datetime.fromtimestamp(data['time_next_update_unix'])
    return Rates(base, data['rates'], last_upd_time, next_upd_time)


@retry(times=3, exceptions=(requests.ConnectionError, requests.Timeout, requests.HTTPError))
def fetch_rates(base: str = 'USD') -> Rates:   # запрос к API + parse_rates
    response = requests.get('https://open.er-api.com/v6/latest/' + base, timeout=10)
    if response.status_code != 200:
        raise ConnectionError('ошибка в запросе')
    
    data = response.json()
    if data.get('result') == 'error':
        raise ApiError(f"API вернул ошибку: {data.get('error-type')}")
    
    return parse_rates(data, base)
