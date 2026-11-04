from models import Rates
from dataclasses import asdict
from datetime import datetime
import requests


def parse_rates(data: dict, base: str) -> Rates:         # словарь из JSON → Rates; без сети
    last_upd_time = datetime.fromtimestamp(data['time_last_update_unix'])
    next_upd_time = datetime.fromtimestamp(data['time_next_update_unix'])
    return Rates(base, data['rates'], last_upd_time, next_upd_time)


def fetch_rates(base: str = 'USD') -> Rates:   # запрос к API + parse_rates
    response = requests.get('https://open.er-api.com/v6/latest/' + base, timeout=10)
    if response.status_code != 200:
        raise ConnectionError('Ошибка соединения')
    else:
        data = response.json()
        return parse_rates(data, base)


print(fetch_rates())