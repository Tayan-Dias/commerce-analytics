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
   |  |- Filters.tsx
   |  |- RevenueChart.tsx
   |  \- TopProductsChart.tsx
   |- services/
   |  \- api.ts
   \- types/
      \- metrics.ts
```

## Current state

- The frontend is implemented with React, TypeScript, Recharts, Axios, and Vite.
- It consumes the backend endpoints for revenue by region and top products.
- It includes loading state, error handling, and a simple category filter.

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
