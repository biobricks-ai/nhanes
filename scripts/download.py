#!/usr/bin/env python
"""
Download ALL NHANES data from CDC.

This script discovers and downloads all available NHANES XPT files across all cycles
and components (Demographics, Laboratory, Examination, Questionnaire).

Data source: https://wwwn.cdc.gov/nchs/nhanes/
"""

import os
import re
import time
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError
import json

# All NHANES continuous survey cycles
CYCLES = [
    "1999-2000",
    "2001-2002",
    "2003-2004",
    "2005-2006",
    "2007-2008",
    "2009-2010",
    "2011-2012",
    "2013-2014",
    "2015-2016",
    "2017-2018",
    "2017-2020",  # Pre-pandemic extended cycle
    "2021-2023",
]

# Data components
COMPONENTS = [
    "Demographics",
    "Dietary",
    "Examination",
    "Laboratory",
    "Questionnaire",
]

# Map cycle to year for URL construction
CYCLE_TO_YEAR = {
    "1999-2000": "1999",
    "2001-2002": "2001",
    "2003-2004": "2003",
    "2005-2006": "2005",
    "2007-2008": "2007",
    "2009-2010": "2009",
    "2011-2012": "2011",
    "2013-2014": "2013",
    "2015-2016": "2015",
    "2017-2018": "2017",
    "2017-2020": "2017",
    "2021-2023": "2021",
}


def get_data_page_url(component: str, cycle: str) -> str:
    """Get the data page URL for a component and cycle."""
    return f"https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component={component}&Cycle={cycle}"


def extract_xpt_links(html: str, base_year: str) -> list:
    """Extract XPT file links from HTML content."""
    # Pattern to match XPT file links
    # Example: href="/Nchs/Nhanes/2015-2016/DEMO_I.XPT"
    pattern = r'href="([^"]*\.XPT)"'
    matches = re.findall(pattern, html, re.IGNORECASE)

    links = []
    for match in matches:
        if match.startswith("/"):
            url = f"https://wwwn.cdc.gov{match}"
        elif match.startswith("http"):
            url = match
        else:
            continue
        links.append(url)

    return list(set(links))  # Remove duplicates


def discover_files_from_page(component: str, cycle: str) -> list:
    """Discover XPT files from a data page."""
    url = get_data_page_url(component, cycle)
    base_year = CYCLE_TO_YEAR.get(cycle, cycle.split("-")[0])

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode("utf-8", errors="ignore")
            return extract_xpt_links(html, base_year)
    except (HTTPError, URLError) as e:
        print(f"  Warning: Could not fetch {url}: {e}")
        return []


def download_file(url: str, output_path: Path) -> bool:
    """Download a file from URL to output path."""
    if output_path.exists():
        print(f"  Skipping (exists): {output_path.name}")
        return True

    print(f"  Downloading: {output_path.name}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as response:
            with open(output_path, "wb") as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"    ERROR: {e}")
        return False


def main():
    download_dir = Path("download")
    download_dir.mkdir(exist_ok=True)

    # Track all discovered files
    all_files = {}

    print("=== NHANES Data Discovery ===\n")

    # Discover files from each component and cycle
    for component in COMPONENTS:
        print(f"\n--- {component} ---")
        for cycle in CYCLES:
            print(f"  Scanning {cycle}...")
            files = discover_files_from_page(component, cycle)
            for url in files:
                filename = url.split("/")[-1]
                # Store with metadata
                all_files[filename] = {
                    "url": url,
                    "component": component,
                    "cycle": cycle,
                }
            time.sleep(0.5)  # Be nice to the server

    print(f"\n=== Discovered {len(all_files)} unique files ===\n")

    # Save manifest
    manifest_path = download_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(all_files, f, indent=2)
    print(f"Saved manifest to {manifest_path}")

    # Download all files
    print("\n=== Downloading Files ===\n")
    success_count = 0
    fail_count = 0

    for filename, info in sorted(all_files.items()):
        output_path = download_dir / filename
        if download_file(info["url"], output_path):
            success_count += 1
        else:
            fail_count += 1
        time.sleep(0.2)  # Rate limit

    print(f"\n=== Download Complete ===")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Total: {len(all_files)}")


if __name__ == "__main__":
    main()
