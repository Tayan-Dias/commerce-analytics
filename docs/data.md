# data/

## Purpose

This folder stores the project datasets used by the assessment.

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

- `raw/` contains the generated source CSV files with controlled inconsistencies for ETL testing.
- `processed/` contains the cleaned CSVs, rejected rows, quality report, and consolidated metrics.

## Notes

The raw files currently available are:

- `categories.csv`
- `customers.csv`
- `inventory.csv`
- `products.csv`
- `sales.csv`

The processed files currently available are:

- `clean_categories.csv`
- `clean_customers.csv`
- `clean_inventory.csv`
- `clean_products.csv`
- `clean_sales.csv`
- `data_quality_report.json`
- `metrics.json`
- `rejected_rows.csv`
