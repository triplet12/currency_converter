from .models import Rates, ConversionRecord
from .core import convert


def format_conversion(amount: float, from_currency: str, to_currency: str,
                      result: float, rate: float, rates: Rates) -> str: 
    date_update = rates.last_upd_time.strftime('%Y-%m-%d')
    return (
        f'{amount:.2f} {from_currency} = {result:.2f} {to_currency}\n'
        f'Курс: 1 {from_currency} = {rate:.4f} {to_currency}, обновлён {date_update}'
    )


def history_format_conversion(record: ConversionRecord) -> str: 

    date = record.created_at.strftime('%Y-%m-%d %H:%M')
    return (
        f'{date}    {record.amount:.2f} {record.from_currency}'
        f'  →  {record.result:.2f} {record.to_currency}'
    )

def rates_format_conversion(base: str, currency: str, rates: Rates) -> str:
    return f'{base.upper()}     {convert(1, base, currency, rates):.4f} {currency.upper()}'