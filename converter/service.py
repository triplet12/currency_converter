import requests
from pathlib import Path
from datetime import datetime
from .models import Rates
from .api import fetch_rates, ApiError
from .storage import load_cached_rates, save_cached_rates


def get_rates(data_dir: Path) -> Rates:
    path = Path(data_dir / 'rates_cache.json')
    cached = load_cached_rates(path)

    if cached and not cached.is_expired(datetime.now()):
        return cached                   

    try:
        fresh = fetch_rates()
    except (requests.RequestException, ApiError):
        if cached is None:
            raise                              
        print(f'Нет связи с сервисом курсов. Используются курсы от {cached.last_upd_time:%d.%m.%Y}')
        return cached                         
    save_cached_rates(fresh, path)
    return fresh    