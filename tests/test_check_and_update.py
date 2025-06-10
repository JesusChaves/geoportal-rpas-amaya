import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.check_and_update import compute_hash, main


def _setup_csv_and_hash(tmp_path, content="some,data\n"):
    """Create a CSV and matching hash file in tmp_path."""
    csv_file = tmp_path / "Geodatabase.csv"
    csv_file.write_text(content)
    hash_file = tmp_path / ".last_csv_hash"
    hash_file.write_text(compute_hash(csv_file))
    return csv_file, hash_file


def test_compute_hash(tmp_path):
    file = tmp_path / "file.txt"
    data = b"hello world"
    file.write_bytes(data)

    expected = __import__('hashlib').md5(data).hexdigest()
    assert compute_hash(file) == expected


def test_main_no_change(tmp_path, monkeypatch, capsys):
    csv_file, hash_file = _setup_csv_and_hash(tmp_path)

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
    # hash should remain unchanged
    assert hash_file.read_text() == compute_hash(csv_file)


def test_main_with_change(tmp_path, monkeypatch):
    csv_file, hash_file = _setup_csv_and_hash(tmp_path)

    monkeypatch.setattr('scripts.check_and_update.CSV_PATH', csv_file)
    monkeypatch.setattr('scripts.check_and_update.HASH_PATH', hash_file)

    called = {'flag': False}

    def fake_update():
        called['flag'] = True

    monkeypatch.setattr('scripts.check_and_update.update_geojson', fake_update)

    # modify csv to change hash
    csv_file.write_text("updated,data\n")

    ret = main()

    assert ret == 0
    assert called['flag'] is True
    assert hash_file.read_text() == compute_hash(csv_file)


def test_main_from_other_cwd(tmp_path, monkeypatch, capsys):
    """main() should locate files relative to the script even when cwd changes."""
    import scripts.check_and_update as mod

    # Use repository CSV but a temporary hash file to avoid side effects
    repo_csv = mod.CSV_PATH
    hash_file = tmp_path / ".last_csv_hash"
    monkeypatch.setattr(mod, "HASH_PATH", hash_file)

    called = {"flag": False}

    def fake_update():
        called["flag"] = True

    monkeypatch.setattr(mod, "update_geojson", fake_update)
    monkeypatch.chdir(tmp_path)

    ret = mod.main()
    captured = capsys.readouterr()

    assert ret == 0
    # The CSV should have been found and processed (i.e. no not-found message)
    assert "CSV not found" not in captured.out
    assert called["flag"] is True
    assert hash_file.read_text() == mod.compute_hash(repo_csv)
