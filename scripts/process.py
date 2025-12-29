#!/usr/bin/env python
"""Convert NHANES XPT files to parquet format.

Simple 1:1 conversion preserving original data structure.
"""

import json
import pandas as pd
from pathlib import Path


def read_xpt(path: Path) -> pd.DataFrame:
    """Read a SAS XPT file into a pandas DataFrame."""
    return pd.read_sas(path, format='xport')


def main():
    download_dir = Path("download")
    brick_dir = Path("brick")
    brick_dir.mkdir(exist_ok=True)

    # Handle both .xpt and .XPT extensions
    xpt_files = sorted(download_dir.glob("*.xpt")) + sorted(download_dir.glob("*.XPT"))
    # Remove duplicates (case-insensitive filesystems)
    seen = set()
    unique_files = []
    for f in xpt_files:
        if f.stem.upper() not in seen:
            seen.add(f.stem.upper())
            unique_files.append(f)
    xpt_files = unique_files

    if not xpt_files:
        print("No XPT files found")
        return

    print(f"Found {len(xpt_files)} XPT files to convert")

    # Load manifest if available for metadata
    manifest_path = download_dir / "manifest.json"
    manifest = {}
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)

    success_count = 0
    fail_count = 0

    for xpt_file in xpt_files:
        output_file = brick_dir / f"{xpt_file.stem}.parquet"

        try:
            print(f"Converting {xpt_file.name}")
            df = read_xpt(xpt_file)
            df.to_parquet(output_file, index=False)
            print(f"  -> {output_file} ({len(df)} rows, {len(df.columns)} columns)")
            success_count += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            fail_count += 1

    # Create catalog from manifest
    if manifest:
        catalog = {}
        for parquet_file in brick_dir.glob("*.parquet"):
            name = parquet_file.stem
            # Find in manifest (case-insensitive)
            for key, info in manifest.items():
                if key.upper().replace(".XPT", "") == name.upper():
                    catalog[name] = {
                        "component": info.get("component", "Unknown"),
                        "cycle": info.get("cycle", "Unknown"),
                    }
                    break
            else:
                catalog[name] = {"component": "Unknown", "cycle": "Unknown"}

        catalog_path = brick_dir / "catalog.json"
        with open(catalog_path, "w") as f:
            json.dump(catalog, f, indent=2, sort_keys=True)
        print(f"\nSaved catalog to {catalog_path}")

    print(f"\nConverted {success_count} files ({fail_count} failed)")


if __name__ == "__main__":
    main()
