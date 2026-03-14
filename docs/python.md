# python/

## Purpose

This folder contains the Python-specific area of the monorepo.

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
- `requirements.txt` defines the Python dependencies.
- `scripts/generate_data.py` generates the raw CSV files stored in `data/raw/`.
- `scripts/etl_pipeline.py` orchestrates the ETL flow.
- `scripts/etl_core.py` concentrates ETL configuration, validation rules, and metric calculations.

## Usage

```bash
pip install -r python/requirements.txt
python python/scripts/generate_data.py
python python/scripts/etl_pipeline.py
```
