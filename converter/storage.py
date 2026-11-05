import os
from datetime import datetime
from contextlib import contextmanager
from pathlib import Path
from json import load, dumps
from dataclasses import asdict
from .models import ConversionRecord, Rates


@contextmanager
def atomic_write(path: Path):
    temp_file = path.with_name(path.name + '.tmp')
    f = temp_file.open('w', encoding='utf-8')
    try:
        yield f
    except Exception:
        f.close()
        temp_file.unlink(missing_ok=True)
        raise
    else:
        f.close()
        os.replace(temp_file, path)


def save_history(records: list, path: Path) -> None:
    result = []
    with atomic_write(path) as f:
        for record in records:
            record_dict = asdict(record)
            record_dict['created_at'] = datetime.isoformat(record_dict['created_at'])
            result.append(record_dict)
        f.write(dumps(result, ensure_ascii=False, indent=4))


def load_history(path: Path) -> list:
    if not os.path.exists():
        return []
    with path.open(encoding='UTF-8') as f:
        result = []
        records = load(f)
        for record in records:
            record['created_at'] = datetime.fromisoformat(record['created_at'])
            result.append(ConversionRecord(**record))
    return result


def load_cached_rates(path: Path) -> Rates | None: 
    if os.path.exists(path):
        with open(path, encoding='UTF-8') as f:
            cached_resp = load(f)
            cached_resp['last_upd_time'] = datetime.fromisoformat(cached_resp['last_upd_time'])
            cached_resp['next_upd_time'] = datetime.fromisoformat(cached_resp['next_upd_time'])
            return Rates(**cached_resp)
    return None


def save_cached_rates(rates: Rates, path: Path) -> None: 
    with atomic_write(path) as f:
        data = asdict(rates)
        data['last_upd_time'] = rates.last_upd_time.isoformat()
        data['next_upd_time'] = rates.next_upd_time.isoformat()
        f.write(dumps(data, ensure_ascii=False, indent=4))
