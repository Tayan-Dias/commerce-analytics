# Aplos Assessment

## Detailed Docs

- [backend/](docs/backend.md)
- [data/](docs/data.md)
- [frontend/](docs/frontend.md)
- [ontology/](docs/ontology.md)
- [python/](docs/python.md)

## Summary

This repository is organized as a monorepo for a retail analytics assessment.

- `python/` generates raw CSV files and runs the ETL pipeline
- `ontology/` stores the conceptual model artifacts for the assessment
- `python/` generates the raw CSV data and runs the ETL pipeline
- `backend/` exposes processed metrics through a simple TypeScript API
- `frontend/` renders the analytics dashboard
- `data/` stores the raw and processed datasets

## Run From Zero

### 1. Install prerequisites

Make sure you have:

- Python 3 installed
- Node.js and npm installed

### 2. Install Python dependencies

From the project root:

```bash
pip install -r python/requirements.txt
```

### 3. Generate the raw CSV files

Still from the project root:

```bash
python python/scripts/generate_data.py
```

This creates the raw files in `data/raw/`.

### 4. Run the ETL pipeline

From the project root:

```bash
python python/scripts/etl_pipeline.py
```

This creates the processed outputs in `data/processed/`, including:

- `clean_*.csv`
- `data_quality_report.json`
- `metrics.json`
- `rejected_rows.csv`

### 5. Start the backend

Open a new terminal:

```bash
cd backend
npm install
npm run dev
```

The backend reads `data/processed/metrics.json` and serves the API on `http://localhost:3000`.

### 6. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend consumes the backend API and renders the dashboard in the Vite dev server.

## API Endpoints

- `GET /api/revenue-by-region`
- `GET /api/top-products`
- `GET /api/customer-churn`
- `GET /api/low-stock-high-sales`
- `GET /api/turnover-by-category`

## Data Flow

1. Python generates raw CSV files in `data/raw/`.
2. The ETL pipeline cleans and consolidates them into `data/processed/`.
3. The backend reads `data/processed/metrics.json` and exposes it through REST endpoints.
4. The frontend consumes the backend endpoints and renders the dashboard charts.
