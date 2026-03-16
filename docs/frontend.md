# frontend/

## Purpose

This folder contains the React dashboard for exploring analytics from the backend API.

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
- It consumes the backend endpoints for revenue by region, top products, customer churn, low stock signals, and turnover by category.
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
- The current dashboard uses:
  - `GET /api/revenue-by-region`
  - `GET /api/top-products`
  - `GET /api/customer-churn`
  - `GET /api/low-stock-high-sales`
  - `GET /api/turnover-by-category`
