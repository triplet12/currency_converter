from dataclasses import dataclass, field
from datetime import datetime



@dataclass(frozen=True)
class Rates:
    base_currency: str
    exchange_dict: dict
    last_upd_time: datetime
    next_upd_time: datetime


@dataclass
class ConversionRecord:
    amount: float
    from_currency: str
    to_currency: str
    rate: float
    result: float
    created_at: datetime = field(default_factory=datetime.now)
