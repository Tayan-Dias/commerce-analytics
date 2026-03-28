# backend/

## Purpose

This folder contains the read-only analytics API that powers the showcase application.

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
   |- types/
   |  \- metrics.types.ts
   \- utils/
      \- loadMetrics.ts
```

## Current state

- The backend is implemented with Node.js, Express, and TypeScript.
- It reads `data/processed/metrics.json`.
- It exposes a read-only REST endpoint for analytics metrics.
- It is intentionally small and easy to review as part of the portfolio narrative.
- The structure is intentionally small: `routes`, `controllers`, `types`, and `utils`.
- The metrics loader uses a 10-second TTL cache to reduce repeated file reads without permanently serving stale data.

## API endpoint

- `GET /api/metrics`

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
