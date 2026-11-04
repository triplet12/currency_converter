import os
from datetime import datetime
from contextlib import contextmanager
from pathlib import Path
from json import load, dumps
from dataclasses import asdict
from .models import ConversionRecord


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
    if os.path.getsize(path) == 0:
        return []
    with path.open(encoding='UTF-8') as f:
        result = []
        records = load(f)
        for record in records:
            record['created_at'] = datetime.fromisoformat(record['created_at'])
            result.append(ConversionRecord(**record))
    return result