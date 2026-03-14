# backend/

## Purpose

This folder contains the read-only analytics API for the project.

## Structure

```text
backend/
|- .gitignore
|- package-lock.json
|- package.json
|- tsconfig.json
\- src/
   |- server.ts
   |- controllers/
   |  \- metrics.controller.ts
   |- routes/
   |  \- metrics.routes.ts
   |- services/
   |  \- metrics.service.ts
   |- types/
   |  \- metrics.types.ts
   \- utils/
      \- loadMetrics.ts
```

## Current state

- The backend is implemented with Node.js, Express, and TypeScript.
- It reads `data/processed/metrics.json`.
- It exposes read-only REST endpoints for analytics metrics.

## API endpoints

- `GET /api/revenue-by-region`
- `GET /api/top-products`
- `GET /api/customer-churn`
- `GET /api/low-stock-high-sales`
- `GET /api/overstock-low-sales`
- `GET /api/turnover-by-category`

## How to run

```bash
cd backend
npm install
npm run dev
```

## Build and start

```bash
cd backend
npm run build
npm start
```

The development server starts on `http://localhost:3000`.
