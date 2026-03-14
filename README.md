# Aplos Assessment

## Summary

This repository is organized as a monorepo with dedicated areas for data, Python utilities, application surfaces, and documentation.

Detailed documentation by root folder:

- [backend/](docs/backend.md)
- [data/](docs/data.md)
- [docs/](docs/docs.md)
- [frontend/](docs/frontend.md)
- [ontology/](docs/ontology.md)
- [python/](docs/python.md)

## Structure

```text
.
|- README.md
|- backend/
|- data/
|  |- processed/
|  |  |- .gitignore
|  |  |- clean_categories.csv
|  |  |- clean_customers.csv
|  |  |- clean_inventory.csv
|  |  |- clean_products.csv
|  |  |- clean_sales.csv
|  |  |- data_quality_report.json
|  |  |- metrics.json
|  |  \- rejected_rows.csv
|  \- raw/
|     |- .gitignore
|     |- categories.csv
|     |- customers.csv
|     |- inventory.csv
|     |- products.csv
|     \- sales.csv
|- docs/
|  |- Aplos Assessment.pdf
|  |- backend.md
|  |- data.md
|  |- docs.md
|  |- frontend.md
|  |- ontology.md
|  \- python.md
|- frontend/
|- ontology/
|  |- ontology-diagram.pdf
|  \- ontology-diagram.png
\- python/
   |- .gitignore
   |- requirements.txt
   \- scripts/
      |- etl_core.py
      |- etl_pipeline.py
      \- generate_data.py
```

## How to run

```bash
pip install -r python/requirements.txt
python python/scripts/generate_data.py
python python/scripts/etl_pipeline.py
```

Raw CSV files are generated in `data/raw/`, and the ETL outputs are written to `data/processed/`.
