#!/usr/bin/env python3
"""Append new records from the local CSV to ``Poligonos_RPAS.json``.

The script keeps track of the last processed row in
``Geodatabase/last_processed_row.txt`` and only converts new rows from
``Geodatabase/Geodatabase.csv`` to GeoJSON features. Conversion logic is
reused from :mod:`update_geojson`.
"""

import csv
import json
from pathlib import Path
import sys

from update_geojson import row_to_geojson_feature

GEOJSON_PATH = Path("Poligonos_RPAS.json")
CSV_PATH = Path("Geodatabase/Geodatabase.csv")
STATE_PATH = Path("Geodatabase/last_processed_row.txt")

def main():
    if not CSV_PATH.exists():
        print(f"CSV not found: {CSV_PATH}")
        return 1

    last = 0
    if STATE_PATH.exists():
        try:
            last = int(STATE_PATH.read_text().strip())
        except Exception:
            pass

    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    total = len(rows)

    if total <= last:
        print("No new rows found.")
        return 0

    new_rows = rows[last:]
    new_features = []
    for row in new_rows:
        feat = row_to_geojson_feature(row)
        if feat:
            new_features.append(feat)

    if not new_features:
        print("No valid new features.")
        STATE_PATH.write_text(str(total))
        return 0

    data = {"type": "FeatureCollection", "features": []}
    if GEOJSON_PATH.exists():
        try:
            with open(GEOJSON_PATH, encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            pass

    features = data.get("features", [])
    features.extend(new_features)
    data["features"] = features

    with open(GEOJSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    STATE_PATH.write_text(str(total))
    print(f"Added {len(new_features)} new features.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
