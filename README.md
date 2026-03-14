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
|  |- .gitignore
|  |- package-lock.json
|  |- package.json
|  |- tsconfig.json
|  \- src/
|     |- server.ts
|     |- controllers/
|     |  \- metrics.controller.ts
|     |- routes/
|     |  \- metrics.routes.ts
|     |- services/
|     |  \- metrics.service.ts
|     |- types/
|     |  \- metrics.types.ts
|     \- utils/
|        \- loadMetrics.ts
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

### Generate and process data

```bash
pip install -r python/requirements.txt
python python/scripts/generate_data.py
python python/scripts/etl_pipeline.py
```

### Run the backend API

```bash
cd backend
npm install
npm run dev
```

The backend reads `data/processed/metrics.json` and serves analytics endpoints on `http://localhost:3000`.

## API Endpoints

- `GET /api/revenue-by-region`
- `GET /api/top-products`
- `GET /api/customer-churn`
- `GET /api/low-stock-high-sales`
- `GET /api/overstock-low-sales`
- `GET /api/turnover-by-category`

## Data Flow

1. Python generates raw CSV files in `data/raw/`.
2. The ETL pipeline cleans and consolidates them into `data/processed/`.
3. The backend reads `data/processed/metrics.json` and exposes it through REST endpoints.
