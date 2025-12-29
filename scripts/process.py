#!/usr/bin/env python
"""Convert NHANES XPT files to parquet format.

Simple 1:1 conversion preserving original data structure.
"""

import pandas as pd
from pathlib import Path


def read_xpt(path: Path) -> pd.DataFrame:
    """Read a SAS XPT file into a pandas DataFrame."""
    return pd.read_sas(path, format='xport')


def main():
    download_dir = Path("download")
    brick_dir = Path("brick")
    brick_dir.mkdir(exist_ok=True)

    xpt_files = sorted(download_dir.glob("*.xpt"))

    for xpt_file in xpt_files:
        print(f"Converting {xpt_file.name}")
        df = read_xpt(xpt_file)

        # Output with same name, just .parquet extension
        output_file = brick_dir / f"{xpt_file.stem}.parquet"
        df.to_parquet(output_file, index=False)
        print(f"  -> {output_file} ({len(df)} rows, {len(df.columns)} columns)")

    print(f"\nConverted {len(xpt_files)} files")


if __name__ == "__main__":
    main()
