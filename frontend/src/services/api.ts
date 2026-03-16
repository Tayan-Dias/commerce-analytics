import axios from "axios";

import type {
  CategoryTurnover,
  CustomerChurn,
  RevenueItem,
  StockMetric,
  TopProduct,
} from "../types/metrics";

const api = axios.create({ baseURL: "http://localhost:3000/api" });

export async function getRevenueByRegion(): Promise<RevenueItem[]> {
  const { data } = await api.get<Record<string, number>>("/revenue-by-region");
  return Object.entries(data).map(([region, revenue]) => ({ region, revenue }));
}

export async function getTopProducts(): Promise<TopProduct[]> {
  const { data } = await api.get<TopProduct[]>("/top-products");
  return data;
}

export async function getCustomerChurn(): Promise<CustomerChurn> {
  const { data } = await api.get<CustomerChurn>("/customer-churn");
  return data;
}

export async function getLowStockHighSales(): Promise<StockMetric[]> {
  const { data } = await api.get<StockMetric[]>("/low-stock-high-sales");
  return data;
}

export async function getTurnoverByCategory(): Promise<CategoryTurnover[]> {
  const { data } = await api.get<CategoryTurnover[]>("/turnover-by-category");
  return data;
}
