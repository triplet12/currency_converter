import os
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime
from contextlib import contextmanager
from pathlib import Path
from json import load, dumps


@contextmanager
def atomic_write(path: Path):
    temp_file = Path('temp_file.tmp')
    f = temp_file.open('w', encoding='UTF-8')
    try:
        yield f
    except Exception as e:
        f.close()
        temp_file.unlink()
        raise e
    else:
        f.close()
        os.replace(temp_file, path)

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


def save_history(records: list, path: Path) -> None:
    result = []
    with atomic_write(path) as f:
        for record in records:
            record_dict = asdict(record)
            record_dict['created_at'] = datetime.isoformat(record_dict['created_at'])
            result.append(record_dict)
        f.write(dumps(result, ensure_ascii=False, indent=4))


def load_history(path: Path) -> list:
    if os.path.getsize(path) == 0:
        return []
    with path.open(encoding='UTF-8') as f:
        result = []
        records = load(f)
        for record in records:
            record['created_at'] = datetime.fromisoformat(record['created_at'])
            result.append(ConversionRecord(**record))
    return result
    


