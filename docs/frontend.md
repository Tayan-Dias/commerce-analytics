# frontend/

## Purpose

This folder contains the React dashboard for the portfolio experience built on top of the backend API.

## Structure

```text
frontend/
|- .gitignore
|- index.html
|- package-lock.json
|- package.json
|- tsconfig.json
\- src/
   |- App.tsx
   |- main.tsx
   |- components/
   |  |- CustomerChurnCard.tsx
   |  |- Filters.tsx
   |  |- Insight.tsx
   |  |- InventorySignals.tsx
   |  |- RevenueChart.tsx
   |  |- TopProductsChart.tsx
   |  \- TurnoverChart.tsx
   |- services/
   |  \- api.ts
   \- types/
      \- metrics.ts
```

## Current state

- The frontend is implemented with React, TypeScript, Recharts, Axios, and Vite.
- The interface is positioned as a Power BI-inspired showcase for analytics storytelling on the web.
- It consumes a single backend metrics endpoint and maps the payload into dashboard-friendly frontend structures.
- It includes loading state, error handling, local category filters, and insight text inside each analytics block.
- The dashboard is organized into five main blocks:
  - `Customer Churn`
  - `Revenue by Region`
  - `Turnover by Category`
  - `Top Selling Products`
  - `Inventory Signals`

## How to run

```bash
cd frontend
npm install
npm run dev
```

## Build and preview

```bash
cd frontend
npm run build
npm start
```

## Notes

- The frontend expects the backend API to be running on `http://localhost:3000`.
- The current dashboard uses `GET /api/metrics`.
