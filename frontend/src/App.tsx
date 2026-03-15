import { useEffect, useState } from "react";

import Filters from "./components/Filters";
import RevenueChart from "./components/RevenueChart";
import TopProductsChart from "./components/TopProductsChart";
import { getRevenueByRegion, getTopProducts } from "./services/api";
import type { RevenueItem, TopProduct } from "./types/metrics";

export default function App() {
  const [revenue, setRevenue] = useState<RevenueItem[]>([]);
  const [topProducts, setTopProducts] = useState<TopProduct[]>([]);
  const [category, setCategory] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    Promise.all([getRevenueByRegion(), getTopProducts()])
      .then(([revenueData, topProductsData]) => {
        setRevenue(revenueData);
        setTopProducts(topProductsData);
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: 32 }}>Loading dashboard...</div>;
  if (error) return <div style={{ padding: 32 }}>Failed to load dashboard data.</div>;

  const categories = [...new Set(topProducts.map((item) => item.category))];
  const filteredProducts =
    category === "All" ? topProducts : topProducts.filter((item) => item.category === category);

  return (
    <main style={{ maxWidth: 960, margin: "0 auto", padding: 32 }}>
      <h1 style={{ marginBottom: 24 }}>Dashboard</h1>
      <Filters categories={categories} value={category} onChange={setCategory} />
      <RevenueChart data={revenue} />
      <TopProductsChart data={filteredProducts} />
    </main>
  );
}
