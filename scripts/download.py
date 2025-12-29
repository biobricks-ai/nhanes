#!/usr/bin/env python
"""Download NHANES Environmental Phenols and Demographics data from CDC."""

import os
import urllib.request
from pathlib import Path

# NHANES Environmental Phenols data URLs
# EPH/EPHPP = Environmental Phenols / Personal Care Products
# Includes benzophenone-3, parabens, BPA, triclosan, etc.
# URL format: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{YEAR}/DataFiles/{FILE}.xpt
NHANES_FILES = {
    # Environmental Phenols - Urine
    "EPH_F": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2009/DataFiles/EPH_F.xpt",  # 2009-2010
    "EPH_G": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/EPH_G.xpt",  # 2011-2012
    "EPHPP_H": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/EPHPP_H.xpt",  # 2013-2014 (renamed)
    "EPHPP_I": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2015/DataFiles/EPHPP_I.xpt",  # 2015-2016
    # Demographics
    "DEMO_F": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2009/DataFiles/DEMO_F.xpt",
    "DEMO_G": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/DEMO_G.xpt",
    "DEMO_H": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/DEMO_H.xpt",
    "DEMO_I": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2015/DataFiles/DEMO_I.xpt",
}


def download_file(url: str, output_path: Path) -> bool:
    """Download a file from URL to output path."""
    print(f"Downloading {url}")
    try:
        urllib.request.urlretrieve(url, output_path)
        print(f"  -> Saved to {output_path}")
        return True
    except Exception as e:
        print(f"  -> ERROR: {e}")
        return False


def main():
    download_dir = Path("download")
    download_dir.mkdir(exist_ok=True)

    success_count = 0
    for name, url in NHANES_FILES.items():
        output_path = download_dir / f"{name}.xpt"
        if download_file(url, output_path):
            success_count += 1

    print(f"\nDownloaded {success_count}/{len(NHANES_FILES)} files")


if __name__ == "__main__":
    main()
