from .models import Rates


class UnknownCurrencyError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

def convert(amount: float, from_currency: str, to_currency: str, rates: Rates) -> float:
    if amount <= 0:
        raise ValueError('Сумма должна быть больше нуля.')
    try:
        from_curr_ex_rate = 1/rates.exchange_dict[from_currency.upper()]
        to_curr_ex_rate = 1/rates.exchange_dict[to_currency.upper()]
    except:
        raise UnknownCurrencyError('Валюта не найдена')
    
    result = (from_curr_ex_rate / to_curr_ex_rate)  * amount
    return result
