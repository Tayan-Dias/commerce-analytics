import { readFile } from "node:fs/promises";
import path from "node:path";

import type { Metrics } from "../types/metrics.types";

const metricsPath = path.resolve(__dirname, "../../../data/processed/metrics.json");
let cachedMetrics: Metrics | null = null;

export async function loadMetrics(): Promise<Metrics> {
  if (cachedMetrics) return cachedMetrics;

  try {
    const fileContent = await readFile(metricsPath, "utf-8");
    cachedMetrics = JSON.parse(fileContent) as Metrics;
    return cachedMetrics;
  } catch {
    throw new Error("Failed to load metrics.json");
  }
}
