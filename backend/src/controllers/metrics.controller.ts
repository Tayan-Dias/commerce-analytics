import type { Request, Response } from "express";

import { metricsService } from "../services/metrics.service";

function handleError(res: Response) {
  return res.status(500).json({ message: "Failed to load metrics data" });
}

export const metricsController = {
  async getRevenueByRegion(_req: Request, res: Response) {
    try { return res.json(await metricsService.getRevenueByRegion()); } catch { return handleError(res); }
  },
  async getTopProducts(_req: Request, res: Response) {
    try { return res.json(await metricsService.getTopProducts()); } catch { return handleError(res); }
  },
  async getCustomerChurn(_req: Request, res: Response) {
    try { return res.json(await metricsService.getCustomerChurn()); } catch { return handleError(res); }
  },
  async getLowStockHighSales(_req: Request, res: Response) {
    try { return res.json(await metricsService.getLowStockHighSales()); } catch { return handleError(res); }
  },
  async getOverstockLowSales(_req: Request, res: Response) {
    try { return res.json(await metricsService.getOverstockLowSales()); } catch { return handleError(res); }
  },
  async getTurnoverByCategory(_req: Request, res: Response) {
    try { return res.json(await metricsService.getTurnoverByCategory()); } catch { return handleError(res); }
  }
};
