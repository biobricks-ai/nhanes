#!/usr/bin/env python
"""Download NHANES Environmental Phenols and Demographics data from CDC."""

import os
import urllib.request
from pathlib import Path

# NHANES Environmental Phenols data URLs
# EPH = Environmental Phenols (includes benzophenone-3, parabens, etc.)
NHANES_FILES = {
    # Environmental Phenols - Urine
    "EPH_F": "https://wwwn.cdc.gov/Nchs/Nhanes/2009-2010/EPH_F.XPT",  # 2009-2010
    "EPH_G": "https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/EPH_G.XPT",  # 2011-2012
    "EPH_H": "https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/EPH_H.XPT",  # 2013-2014
    "EPH_I": "https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/EPH_I.XPT",  # 2015-2016
    # Demographics
    "DEMO_F": "https://wwwn.cdc.gov/Nchs/Nhanes/2009-2010/DEMO_F.XPT",
    "DEMO_G": "https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/DEMO_G.XPT",
    "DEMO_H": "https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/DEMO_H.XPT",
    "DEMO_I": "https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.XPT",
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
        output_path = download_dir / f"{name}.XPT"
        if download_file(url, output_path):
            success_count += 1

    print(f"\nDownloaded {success_count}/{len(NHANES_FILES)} files")


if __name__ == "__main__":
    main()
