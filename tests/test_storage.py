from pathlib import Path

from converter.models import ConversionRecord
from converter.storage import load_history, save_history


def test_load_history_no_file(tmp_path: Path):
    path = tmp_path / 'history.json'      
    assert load_history(path) == []


def test_load_history_empty_file(tmp_path: Path):
    path = tmp_path / 'history.json'
    path.write_text('', encoding='utf-8')  
    assert load_history(path) == []


def test_save_and_load_history(tmp_path: Path):
    path = tmp_path / 'history.json'
    records = [
        ConversionRecord(100, 'USD', 'RUB', 81.4, 8140),
        ConversionRecord(50, 'EUR', 'USD', 1.12, 56),
    ]

    save_history(records, path)
    assert records == load_history(path)