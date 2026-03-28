import { readFile } from "node:fs/promises";
import path from "node:path";

import type { Metrics } from "../types/metrics.types";

const metricsPath = path.resolve(__dirname, "../../../data/processed/metrics.json");
const CACHE_TTL_MS = 10_000;

let cachedMetrics: Metrics | null = null;
let cacheExpiresAt = 0;
let inflightLoad: Promise<Metrics> | null = null;

export async function loadMetrics(): Promise<Metrics> {
  const now = Date.now();

  if (cachedMetrics && now < cacheExpiresAt) {
    return cachedMetrics;
  }

  if (inflightLoad) {
    return inflightLoad;
  }

  inflightLoad = readFile(metricsPath, "utf-8")
    .then((fileContent) => {
      cachedMetrics = JSON.parse(fileContent) as Metrics;
      cacheExpiresAt = Date.now() + CACHE_TTL_MS;
      return cachedMetrics;
    })
    .catch(() => {
      throw new Error("Failed to load metrics.json");
    })
    .finally(() => {
      inflightLoad = null;
    });

  return inflightLoad;
}
