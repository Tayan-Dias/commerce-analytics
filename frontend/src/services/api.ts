import axios from "axios";

import type { RevenueItem, TopProduct } from "../types/metrics";

const api = axios.create({ baseURL: "http://localhost:3000/api" });

export async function getRevenueByRegion(): Promise<RevenueItem[]> {
  const { data } = await api.get<Record<string, number>>("/revenue-by-region");
  return Object.entries(data).map(([region, revenue]) => ({ region, revenue }));
}

export async function getTopProducts(): Promise<TopProduct[]> {
  const { data } = await api.get<TopProduct[]>("/top-products");
  return data;
}
