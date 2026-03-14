# python/

## Purpose

This folder contains the Python data generation and ETL area of the monorepo.

## Structure

```text
python/
|- .gitignore
|- requirements.txt
\- scripts/
   |- etl_core.py
   |- etl_pipeline.py
   \- generate_data.py
```

## Current state

- `.gitignore` ignores local Python cache files and virtual environments inside this folder.
- `requirements.txt` defines the Python dependency used by the scripts.
- `scripts/generate_data.py` generates the raw CSV files in `data/raw/`.
- `scripts/etl_pipeline.py` orchestrates the ETL flow and writes outputs to `data/processed/`.
- `scripts/etl_core.py` contains ETL configuration, validation rules, and metric calculations.

## How to install

```bash
pip install -r python/requirements.txt
```

## How to generate raw data

```bash
python python/scripts/generate_data.py
```

## How to run the ETL

```bash
python python/scripts/etl_pipeline.py
```

## Execution order

1. Run `generate_data.py` to refresh the raw CSV files.
2. Run `etl_pipeline.py` to produce cleaned files, rejected rows, quality reporting, and analytics metrics.
