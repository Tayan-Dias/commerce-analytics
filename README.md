# Commerce Analytics Showcase

## Overview

This repository is an open-source portfolio project that demonstrates an end-to-end retail analytics stack.
It combines Python ETL, a Node.js API, a React dashboard, and data modeling artifacts to present a Power BI-inspired analytics experience built for the web.

## Detailed Docs

- [backend/](docs/backend.md)
- [data/](docs/data.md)
- [frontend/](docs/frontend.md)
- [ontology/](docs/ontology.md)
- [python/](docs/python.md)

## What This Project Demonstrates

- React + TypeScript dashboard development with reusable chart components
- Node.js + Express API design for analytics delivery
- ETL and data quality workflows in Python
- Data modeling and ontology documentation for the domain
- A complete local stack that can be used as a technical portfolio piece

## Repository Structure

- `python/` generates source CSV files and runs the ETL pipeline
- `ontology/` stores the conceptual model artifacts for the retail domain
- `backend/` exposes processed metrics through a TypeScript REST API
- `frontend/` renders the analytics dashboard
- `data/` stores the raw and processed datasets

## Run Locally

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

## API Endpoint

- `GET /api/metrics`

## Data Flow

1. Python generates raw CSV files in `data/raw/`.
2. The ETL pipeline cleans and consolidates them into `data/processed/`.
3. The backend reads `data/processed/metrics.json` and exposes it through REST endpoints.
4. The frontend consumes the consolidated backend metrics endpoint and renders the dashboard charts.
