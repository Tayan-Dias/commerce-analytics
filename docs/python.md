# python/

## Purpose

This folder contains the Python-specific area of the monorepo.

## Structure

```text
python/
|- requirements.txt
\- scripts/
   \- generate_data.py
```

## Current state

- `requirements.txt` defines the Python dependencies.
- `scripts/generate_data.py` generates the CSV files stored in `data/raw/`.

## Usage

```bash
pip install -r python/requirements.txt
python python/scripts/generate_data.py
```
