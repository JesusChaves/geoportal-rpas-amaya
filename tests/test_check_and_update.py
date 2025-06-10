import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.check_and_update import compute_hash, main


def test_compute_hash(tmp_path):
    file = tmp_path / "file.txt"
    data = b"hello world"
    file.write_bytes(data)

    expected = __import__('hashlib').md5(data).hexdigest()
    assert compute_hash(file) == expected


def test_main_no_change(tmp_path, monkeypatch, capsys):
    csv_file = tmp_path / "Geodatabase.csv"
    csv_file.write_text("some,data\n")

    hash_val = compute_hash(csv_file)
    hash_file = tmp_path / ".last_csv_hash"
    hash_file.write_text(hash_val)

    monkeypatch.setattr('scripts.check_and_update.CSV_PATH', csv_file)
    monkeypatch.setattr('scripts.check_and_update.HASH_PATH', hash_file)

    called = {'flag': False}

    def fake_update():
        called['flag'] = True

    monkeypatch.setattr('scripts.check_and_update.update_geojson', fake_update)

    ret = main()
    captured = capsys.readouterr()

    assert ret == 0
    assert "CSV unchanged" in captured.out
    assert called['flag'] is False
