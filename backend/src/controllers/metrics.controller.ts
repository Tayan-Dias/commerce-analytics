import type { RequestHandler, Response } from "express";

import type { Metrics } from "../types/metrics.types";
import { loadMetrics } from "../utils/loadMetrics";

function handleError(res: Response) {
  return res.status(500).json({ message: "Failed to load metrics data" });
}

function createMetricsHandler(section: keyof Metrics): RequestHandler {
  return async (_req, res) => {
    try {
      const metrics = await loadMetrics();
      return res.json(metrics[section]);
    } catch {
      return handleError(res);
    }
  };
}

export const metricsController = {
  getRevenueByRegion: createMetricsHandler("revenue_by_region"),
  getTopProducts: createMetricsHandler("top_selling_products"),
  getCustomerChurn: createMetricsHandler("customer_churn"),
  getLowStockHighSales: createMetricsHandler("low_stock_high_sales"),
  getOverstockLowSales: createMetricsHandler("overstock_low_sales"),
  getTurnoverByCategory: createMetricsHandler("turnover_by_category"),
};
