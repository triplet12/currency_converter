import requests
import argparse
from pathlib import Path
from datetime import datetime
from .models import Rates
from .api import fetch_rates, ApiError
from .storage import load_cached_rates, save_cached_rates
from .core import convert


DATA_DIR = Path.home() / '.currency_converter'


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

def format_conversion(amount: float, from_currency: str, to_currency: str,
                      result: float, rate: float, rates: Rates) -> str: 
    date_update = rates.last_upd_time.strftime('%Y-%m-%d')
    return (
        f'{amount:.2f} {from_currency} = {result:.2f} {to_currency}\n'
        f'Курс: 1 {from_currency} = {rate} {to_currency}, обновлён {date_update}'
    )


def main(argv: list[str] | None = None) -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser(prog='conveter')
    subparsers = parser.add_subparsers(dest='command', required=True)
    convert_parser = subparsers.add_parser('convert', help='конвертировать валюту')

    convert_parser.add_argument('amount', type=float)
    convert_parser.add_argument('from_currency', type=str)
    convert_parser.add_argument('to_currency', type=str)


    args = parser.parse_args(argv)
    if args.command == 'convert':
        rate = get_rates(DATA_DIR)
        result = convert(args.amount, args.from_currency, args.to_currency, rate)
        format_output = format_conversion(args.amount, args.from_currency, args.to_currency, result,
                                   rate.exchange_dict[args.to_currency], rate)
        print(format_output)

