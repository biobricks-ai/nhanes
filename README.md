# NHANES

Comprehensive NHANES (National Health and Nutrition Examination Survey) data from CDC, converted to parquet format.

## Description

This brick contains the complete NHANES continuous survey data (1999-2023) converted 1:1 from SAS transport (XPT) format to parquet. Each source file maps directly to one parquet file with no transformations.

**Total: 1575 files across all components and cycles**

## Data Components

| Component | Files | Description |
|-----------|-------|-------------|
| Demographics | 12 | Population characteristics, sample weights |
| Dietary | 125 | Food and nutrient intake data |
| Examination | 182 | Physical measurements, clinical assessments |
| Laboratory | 750 | Biomarkers, blood/urine chemistry |
| Questionnaire | 506 | Health conditions, behaviors, exposures |

## Survey Cycles

Data spans continuous NHANES from 1999-2000 through 2021-2023:
- 1999-2000, 2001-2002, 2003-2004, 2005-2006, 2007-2008
- 2009-2010, 2011-2012, 2013-2014, 2015-2016, 2017-2018
- 2017-2020 (pre-pandemic extended cycle)
- 2021-2023 (post-pandemic)

## File Naming Convention

Files follow NHANES naming convention with cycle suffix:
- `DEMO_I.parquet` = Demographics, 2015-2016
- `BIOPRO_J.parquet` = Standard Biochemistry, 2017-2018
- `EPHPP_H.parquet` = Environmental Phenols, 2013-2014

The `catalog.json` file in the brick directory maps each file to its component and cycle.

## Usage

```python
import biobricks as bb

bb.install("nhanes")
nhanes = bb.load("nhanes")

# List available files
import json
with open(nhanes.brick_path / "catalog.json") as f:
    catalog = json.load(f)
print(f"Total files: {len(catalog)}")
```

Or directly with pandas:

```python
import pandas as pd

# Load laboratory data
biopro = pd.read_parquet("brick/BIOPRO_I.parquet")

# Load demographics for the same cycle
demo = pd.read_parquet("brick/DEMO_I.parquet")

# Merge by participant ID
merged = pd.merge(biopro, demo, on="SEQN")
```

## Key Laboratory Files

| File Pattern | Description |
|--------------|-------------|
| `BIOPRO_*` | Standard biochemistry (liver, kidney, etc.) |
| `CBC_*` | Complete blood count |
| `EPHPP_*` / `EPH_*` | Environmental phenols, BPA, parabens |
| `PFAS_*` | Per/polyfluoroalkyl substances |
| `PHTHTE_*` | Phthalates |
| `PAH_*` | Polycyclic aromatic hydrocarbons |
| `PBCD_*` | Lead, cadmium, mercury |
| `COT_*` / `COTNAL_*` | Cotinine (smoking biomarker) |
| `GHB_*` | Glycohemoglobin (diabetes) |
| `HDL_*` / `TCHOL_*` / `TRIGLY_*` | Lipids |

## Source

Data from CDC National Center for Health Statistics:
https://wwwn.cdc.gov/nchs/nhanes/

Documentation for each file is available at:
https://wwwn.cdc.gov/Nchs/Nhanes/Search/DataPage.aspx

## License

NHANES data is public domain (U.S. Government Work).
