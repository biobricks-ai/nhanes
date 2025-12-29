# NHANES Environmental Phenols

NHANES (National Health and Nutrition Examination Survey) Environmental Phenols data from CDC.

## Description

This brick contains urinary biomarker data for environmental phenols including:
- **Benzophenone-3 (BP-3/oxybenzone)** - UV filter in sunscreens (URXBP3)
- **Bisphenol A (BPA)** - plasticizer (URXBPH)
- **Parabens** - preservatives (methylparaben, propylparaben, etc.)
- **Triclosan** - antimicrobial agent (URXTRS)

Data spans NHANES cycles 2009-2010 through 2015-2016.

## Data Files

- `environmental_phenols.parquet` - Raw EPH data from all cycles
- `demographics.parquet` - Demographics data for all participants
- `phenols_with_demographics.parquet` - Merged dataset with key variables

## Key Variables

### Environmental Phenols
| Variable | Description |
|----------|-------------|
| SEQN | Respondent sequence number |
| URXBP3 | Urinary Benzophenone-3 (ng/mL) |
| URDBP3LC | Benzophenone-3 detection limit flag |
| URXBPH | Urinary Bisphenol A (ng/mL) |
| URXMPB | Urinary Methylparaben (ng/mL) |
| URXPPB | Urinary Propylparaben (ng/mL) |
| URXTRS | Urinary Triclosan (ng/mL) |

### Demographics
| Variable | Description |
|----------|-------------|
| RIAGENDR | Gender (1=Male, 2=Female) |
| RIDAGEYR | Age in years |
| RIDRETH1 | Race/ethnicity |
| INDFMPIR | Family income to poverty ratio |

## Usage

```python
import biobricks as bb

bb.install("nhanes-environmental-phenols")
bb.load("nhanes-environmental-phenols")
```

Or directly with pandas:

```python
import pandas as pd

phenols = pd.read_parquet("brick/phenols_with_demographics.parquet")
print(phenols.head())
```

## Source

Data from CDC National Center for Health Statistics:
https://wwwn.cdc.gov/nchs/nhanes/

## License

NHANES data is public domain (U.S. Government Work).
