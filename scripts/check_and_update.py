#!/usr/bin/env python3
"""Check CSV for changes and update GeoJSON if needed."""

from pathlib import Path
import hashlib
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))

from update_geojson import update_geojson

# Resolve paths relative to the repository root so the script can be executed
# from any working directory.
CSV_PATH = ROOT_DIR / "Geodatabase" / "Geodatabase.csv"
HASH_PATH = ROOT_DIR / "Geodatabase" / ".last_csv_hash"


def compute_hash(path: Path) -> str:
    """Return the MD5 hash of a file."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not CSV_PATH.exists():
        print(f"CSV not found: {CSV_PATH}")
        return 1

    current = compute_hash(CSV_PATH)
    last = None
    if HASH_PATH.exists():
        try:
            last = HASH_PATH.read_text().strip()
        except Exception:
            pass

    print(f"Current hash: {current}, Last hash: {last}")

    if current == last:
        print("CSV unchanged. Nothing to do.")
        return 0

    update_geojson()
    HASH_PATH.write_text(current)
    print("GeoJSON regenerated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
