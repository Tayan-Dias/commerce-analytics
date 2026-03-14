# data/

## Purpose

This folder stores the assessment datasets used by the Python ETL and the backend API.

## Structure

```text
data/
|- processed/
|  |- .gitignore
|  |- clean_categories.csv
|  |- clean_customers.csv
|  |- clean_inventory.csv
|  |- clean_products.csv
|  |- clean_sales.csv
|  |- data_quality_report.json
|  |- metrics.json
|  \- rejected_rows.csv
\- raw/
   |- .gitignore
   |- categories.csv
   |- customers.csv
   |- inventory.csv
   |- products.csv
   \- sales.csv
```

## Current state

- `raw/` contains generated source CSV files with a few controlled inconsistencies.
- `processed/` contains cleaned CSVs, rejected rows, a quality report, and consolidated metrics.

## How to generate the data

```bash
python python/scripts/generate_data.py
```

## How to process the data

```bash
python python/scripts/etl_pipeline.py
```

## Notes

`metrics.json` is the file consumed by the backend API.
