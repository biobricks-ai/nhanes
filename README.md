# NHANES

NHANES (National Health and Nutrition Examination Survey) data from CDC, converted to parquet format.

## Description

This brick contains NHANES laboratory and demographic data files converted 1:1 from SAS transport (XPT) format to parquet.

Current data includes Environmental Phenols and Demographics from cycles 2009-2016.

## Data Files

Each source XPT file is converted to a corresponding parquet file:

### Environmental Phenols (Urine)
| File | Cycle | Description |
|------|-------|-------------|
| `EPH_F.parquet` | 2009-2010 | Environmental Phenols |
| `EPH_G.parquet` | 2011-2012 | Environmental Phenols |
| `EPHPP_H.parquet` | 2013-2014 | Personal Care Products & Phenols |
| `EPHPP_I.parquet` | 2015-2016 | Personal Care Products & Phenols |

### Demographics
| File | Cycle | Description |
|------|-------|-------------|
| `DEMO_F.parquet` | 2009-2010 | Demographic Variables |
| `DEMO_G.parquet` | 2011-2012 | Demographic Variables |
| `DEMO_H.parquet` | 2013-2014 | Demographic Variables |
| `DEMO_I.parquet` | 2015-2016 | Demographic Variables |

## Usage

```python
import biobricks as bb

bb.install("nhanes")
bb.load("nhanes")
```

Or directly with pandas:

```python
import pandas as pd

# Load a specific cycle
eph_2015 = pd.read_parquet("brick/EPHPP_I.parquet")
demo_2015 = pd.read_parquet("brick/DEMO_I.parquet")

# Merge phenols with demographics
merged = pd.merge(eph_2015, demo_2015, on="SEQN")
```

## Source

Data from CDC National Center for Health Statistics:
https://wwwn.cdc.gov/nchs/nhanes/

Documentation for each file is available at:
https://wwwn.cdc.gov/Nchs/Nhanes/Search/DataPage.aspx

## License

NHANES data is public domain (U.S. Government Work).
