import axios from "axios";

import type {
  CategoryTurnover,
  CustomerChurn,
  RevenueItem,
  StockMetric,
  TopProduct,
} from "../types/metrics";

const api = axios.create({ baseURL: "http://localhost:3000/api" });

interface DashboardMetricsResponse {
  revenue_by_region: Record<string, number>;
  top_selling_products: TopProduct[];
  customer_churn: CustomerChurn;
  low_stock_high_sales: StockMetric[];
  turnover_by_category: CategoryTurnover[];
}

export interface DashboardMetrics {
  revenue: RevenueItem[];
  topProducts: TopProduct[];
  customerChurn: CustomerChurn;
  lowStockHighSales: StockMetric[];
  turnoverByCategory: CategoryTurnover[];
}

export async function getDashboardMetrics(): Promise<DashboardMetrics> {
  const { data } = await api.get<DashboardMetricsResponse>("/metrics");

  return {
    revenue: Object.entries(data.revenue_by_region).map(([region, revenue]) => ({ region, revenue })),
    topProducts: data.top_selling_products,
    customerChurn: data.customer_churn,
    lowStockHighSales: data.low_stock_high_sales,
    turnoverByCategory: data.turnover_by_category,
  };
}
