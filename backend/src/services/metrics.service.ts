import { loadMetrics } from "../utils/loadMetrics";

export const metricsService = {
  async getRevenueByRegion() { return (await loadMetrics()).revenue_by_region; },
  async getTopProducts() { return (await loadMetrics()).top_selling_products; },
  async getCustomerChurn() { return (await loadMetrics()).customer_churn; },
  async getLowStockHighSales() { return (await loadMetrics()).low_stock_high_sales; },
  async getOverstockLowSales() { return (await loadMetrics()).overstock_low_sales; },
  async getTurnoverByCategory() { return (await loadMetrics()).turnover_by_category; }
};
