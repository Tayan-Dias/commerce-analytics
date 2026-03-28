import type { Request, Response } from "express";

import { loadMetrics } from "../utils/loadMetrics";

function handleError(res: Response) {
  return res.status(500).json({ message: "Failed to load metrics data" });
}

export const metricsController = {
  async getMetrics(_req: Request, res: Response) {
    try {
      const metrics = await loadMetrics();
      return res.json(metrics);
    } catch {
      return handleError(res);
    }
  },
};
