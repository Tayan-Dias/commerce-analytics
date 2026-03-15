import type { Request, Response } from "express";

import type { Metrics } from "../types/metrics.types";
import { loadMetrics } from "../utils/loadMetrics";

function handleError(res: Response) {
  return res.status(500).json({ message: "Failed to load metrics data" });
}

async function sendMetricsSection(res: Response, section: keyof Metrics) {
  try {
    const metrics = await loadMetrics();
    return res.json(metrics[section]);
  } catch {
    return handleError(res);
  }
}

export const metricsController = {
  async getRevenueByRegion(_req: Request, res: Response) {
    return sendMetricsSection(res, "revenue_by_region");
  },
  async getTopProducts(_req: Request, res: Response) {
    return sendMetricsSection(res, "top_selling_products");
  },
  async getCustomerChurn(_req: Request, res: Response) {
    return sendMetricsSection(res, "customer_churn");
  },
  async getLowStockHighSales(_req: Request, res: Response) {
    return sendMetricsSection(res, "low_stock_high_sales");
  },
  async getOverstockLowSales(_req: Request, res: Response) {
    return sendMetricsSection(res, "overstock_low_sales");
  },
  async getTurnoverByCategory(_req: Request, res: Response) {
    return sendMetricsSection(res, "turnover_by_category");
  },
};
