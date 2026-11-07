import requests
import argparse
from pathlib import Path
from datetime import datetime
from .models import Rates, ConversionRecord
from .api import fetch_rates, ApiError
from .storage import load_history, save_history, append_history
from .storage import load_cached_rates, save_cached_rates
from .core import convert, UnknownCurrencyError
from .formatting import format_conversion, history_format_conversion


DATA_DIR = Path.home() / '.currency_converter'
HISTORY_FILE = DATA_DIR / 'history.json'


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


def main(argv: list[str] | None = None) -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser(prog='convertor')
    subparsers = parser.add_subparsers(dest='command', required=True)

    convert_parser = subparsers.add_parser('convert', help='конвертировать валюту')
    history_parser = subparsers.add_parser('history', help='Показать историю')

    convert_parser.add_argument('amount', type=float)
    convert_parser.add_argument('from_currency', type=str)
    convert_parser.add_argument('to_currency', type=str)

    history_parser.add_argument('--last', type=int, default=10)
    history_parser.add_argument('--clear', action='store_true')

    args = parser.parse_args(argv)

    if args.command == 'convert':
        try:
            rates = get_rates(DATA_DIR)
            from_currency = args.from_currency.upper()
            to_currency = args.to_currency.upper()
            rate = convert(1,from_currency, to_currency, rates)
            result = convert(args.amount, from_currency, to_currency, rates)
            record = ConversionRecord(args.amount, from_currency, to_currency, rate, result)
            
            format_output = format_conversion(args.amount, from_currency, to_currency,
                                               result, rate, rates)
            append_history(record, HISTORY_FILE)
            print(HISTORY_FILE)
            
            print(format_output)
        except (UnknownCurrencyError, ValueError, ApiError) as e:
            print(f'Ошибка: {e}')
            return 1
        except requests.RequestException:
            print('Ошибка: нет связи с сервисом курсов')
            return 1
        return 0   

    if args.command == 'history':
        if args.clear:
            save_history([], HISTORY_FILE)
            print('История очищена.')
            return 0

        records = load_history(HISTORY_FILE)
        if not records:
            print('Истории нет.')
        for record in records[-1:-1*args.last-1:-1]:
            print(history_format_conversion(record))
        return 0
        
    return 0
