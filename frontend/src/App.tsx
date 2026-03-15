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
  let filteredProducts = topProducts;

  if (category !== "All") {
    filteredProducts = topProducts.filter((item) => item.category === category);
  }

  return (
    <main style={{ maxWidth: 960, margin: "0 auto", padding: 32 }}>
      <header
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          flexWrap: "wrap",
          gap: 16,
          padding: 24,
          marginBottom: 24,
          borderRadius: 12,
          background: "#fff",
          color: "#1f2937",
          border: "1px solid #e5e7eb",
          boxShadow: "0 10px 24px rgba(15, 23, 42, 0.06)"
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <img
            src="/aplos_innovation_logo.jpg"
            alt="Aplos Assessment logo"
            style={{
              width: 64,
              height: 64,
              borderRadius: 12,
              flexShrink: 0,
              objectFit: "cover",
            }}
          />
          <div>
            <p
              style={{
                margin: 0,
                fontSize: 12,
                letterSpacing: 2,
                textTransform: "uppercase",
                color: "#6b7280"
              }}
            >
              Retail Analytics
            </p>
            <h1 style={{ margin: "6px 0 8px", fontSize: 32 }}>Aplos Assessment | Dashboard</h1>
            <p style={{ margin: 0, color: "#4b5563", lineHeight: 1.5 }}>
              A quick view of revenue, products, and stock for the Aplos Assessment.
            </p>
          </div>
        </div>
        <Filters categories={categories} value={category} onChange={setCategory} />
      </header>

      <RevenueChart data={revenue} />
      <TopProductsChart data={filteredProducts} />
    </main>
  );
}
