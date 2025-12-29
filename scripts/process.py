#!/usr/bin/env python
"""Process NHANES XPT files into parquet format."""

import pandas as pd
from pathlib import Path


def read_xpt(path: Path) -> pd.DataFrame:
    """Read a SAS XPT file into a pandas DataFrame."""
    return pd.read_sas(path, format='xport')


def process_environmental_phenols():
    """Process Environmental Phenols data into combined parquet files."""
    download_dir = Path("download")
    brick_dir = Path("brick")
    brick_dir.mkdir(exist_ok=True)

    # Process EPH files (Environmental Phenols)
    # Note: Pattern matches both EPH_*.xpt and EPHPP_*.xpt (renamed starting 2013-2014)
    eph_files = sorted(list(download_dir.glob("EPH_*.xpt")) + list(download_dir.glob("EPHPP_*.xpt")))
    eph_dfs = []

    cycle_map = {
        "EPH_F": "2009-2010",
        "EPH_G": "2011-2012",
        "EPHPP_H": "2013-2014",  # Renamed in 2013-2014
        "EPHPP_I": "2015-2016",
    }

    for f in eph_files:
        cycle = cycle_map.get(f.stem, f.stem)
        print(f"Processing {f.name} ({cycle})")
        df = read_xpt(f)
        df["CYCLE"] = cycle
        eph_dfs.append(df)

    if eph_dfs:
        eph_combined = pd.concat(eph_dfs, ignore_index=True)
        eph_output = brick_dir / "environmental_phenols.parquet"
        eph_combined.to_parquet(eph_output, index=False)
        print(f"Saved {len(eph_combined)} rows to {eph_output}")

        # Print column info
        print(f"\nEnvironmental Phenols columns:")
        for col in eph_combined.columns:
            print(f"  - {col}")

    # Process DEMO files (Demographics)
    demo_files = sorted(download_dir.glob("DEMO_*.xpt"))
    demo_dfs = []

    demo_cycle_map = {
        "DEMO_F": "2009-2010",
        "DEMO_G": "2011-2012",
        "DEMO_H": "2013-2014",
        "DEMO_I": "2015-2016",
    }

    for f in demo_files:
        cycle = demo_cycle_map.get(f.stem, f.stem)
        print(f"\nProcessing {f.name} ({cycle})")
        df = read_xpt(f)
        df["CYCLE"] = cycle
        demo_dfs.append(df)

    if demo_dfs:
        demo_combined = pd.concat(demo_dfs, ignore_index=True)
        demo_output = brick_dir / "demographics.parquet"
        demo_combined.to_parquet(demo_output, index=False)
        print(f"Saved {len(demo_combined)} rows to {demo_output}")

    # Create a merged dataset with key variables
    if eph_dfs and demo_dfs:
        # Key EPH variables for benzophenone-3 analysis
        eph_key_cols = ['SEQN', 'CYCLE', 'URXBP3', 'URDBP3LC', 'URXBPH', 'URDBPHLC',
                        'URX4TO', 'URD4TOLC', 'URXBUP', 'URDBUPLC', 'URXEPB', 'URDEPBLC',
                        'URXMPB', 'URDMPBLC', 'URXPPB', 'URDPPBLC', 'URXTRS', 'URDTRSLC']

        # Filter to columns that exist
        eph_cols = [c for c in eph_key_cols if c in eph_combined.columns]
        eph_subset = eph_combined[eph_cols].copy()

        # Key demographic variables
        demo_key_cols = ['SEQN', 'CYCLE', 'RIAGENDR', 'RIDAGEYR', 'RIDRETH1', 'RIDRETH3',
                         'DMDEDUC2', 'DMDEDUC3', 'INDFMPIR', 'WTINT2YR', 'WTMEC2YR']
        demo_cols = [c for c in demo_key_cols if c in demo_combined.columns]
        demo_subset = demo_combined[demo_cols].copy()

        # Merge on SEQN and CYCLE
        merged = pd.merge(eph_subset, demo_subset, on=['SEQN', 'CYCLE'], how='inner')
        merged_output = brick_dir / "phenols_with_demographics.parquet"
        merged.to_parquet(merged_output, index=False)
        print(f"\nSaved merged dataset with {len(merged)} rows to {merged_output}")


def main():
    print("Processing NHANES Environmental Phenols data\n")
    process_environmental_phenols()
    print("\nDone!")


if __name__ == "__main__":
    main()
