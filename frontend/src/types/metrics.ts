export interface RevenueItem {
  region: string;
  revenue: number;
}

export interface TopProduct {
  product_id: number | string;
  category: string;
  total_quantity_sold: number;
}
