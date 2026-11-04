from models import Rates


class UnknownCurrencyError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

def convert(amount: float, from_currency: str, to_currency: str, rates: Rates) -> float:
    if amount <= 0:
        raise UnknownCurrencyError('Сумма должна быть больше нуля.')
    try:
        from_curr_ex_rate = 1/rates.exchange_dict['rates'][from_currency]
        to_curr_ex_rate = 1/rates.exchange_dict['rates'][to_currency]
    except:
        raise ValueError('Валюта не найдена')
    
    result = to_curr_ex_rate / from_curr_ex_rate
    return result