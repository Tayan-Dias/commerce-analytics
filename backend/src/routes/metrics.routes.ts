import { Router } from "express";

import { metricsController } from "../controllers/metrics.controller";

const router = Router();

router.get("/revenue-by-region", metricsController.getRevenueByRegion);
router.get("/top-products", metricsController.getTopProducts);
router.get("/customer-churn", metricsController.getCustomerChurn);
router.get("/low-stock-high-sales", metricsController.getLowStockHighSales);
router.get("/overstock-low-sales", metricsController.getOverstockLowSales);
router.get("/turnover-by-category", metricsController.getTurnoverByCategory);

export default router;
