export interface RevenueItem {
  region: string;
  revenue: number;
}

export interface TopProduct {
  product_id: number | string;
  category: string;
  total_quantity_sold: number;
}

export interface CustomerChurn {
  total_customers: number;
  active_customers: number;
  churned_customers: number;
  churn_rate: number;
}

export interface StockMetric {
  product_id: number | string;
  category: string;
  current_stock: number;
  total_quantity_sold: number;
}

export interface CategoryTurnover {
  category: string;
  total_quantity_sold: number;
  current_stock: number;
  turnover_rate: number;
}
