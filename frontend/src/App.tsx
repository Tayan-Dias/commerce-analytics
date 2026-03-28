import { useEffect, useState } from "react";

import CustomerChurnCard from "./components/CustomerChurnCard";
import InventorySignals from "./components/InventorySignals";
import RevenueChart from "./components/RevenueChart";
import TopProductsChart from "./components/TopProductsChart";
import TurnoverChart from "./components/TurnoverChart";
import { getDashboardMetrics } from "./services/api";
import type {
  CategoryTurnover,
  CustomerChurn,
  RevenueItem,
  StockMetric,
  TopProduct,
} from "./types/metrics";

export default function App() {
  const [revenue, setRevenue] = useState<RevenueItem[]>([]);
  const [topProducts, setTopProducts] = useState<TopProduct[]>([]);
  const [customerChurn, setCustomerChurn] = useState<CustomerChurn | null>(null);
  const [lowStockHighSales, setLowStockHighSales] = useState<StockMetric[]>([]);
  const [turnoverByCategory, setTurnoverByCategory] = useState<CategoryTurnover[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    getDashboardMetrics()
      .then(({ revenue, topProducts, customerChurn, lowStockHighSales, turnoverByCategory }) => {
        setRevenue(revenue);
        setTopProducts(topProducts);
        setCustomerChurn(customerChurn);
        setLowStockHighSales(lowStockHighSales);
        setTurnoverByCategory(turnoverByCategory);
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ maxWidth: 1200, margin: "0 auto", padding: 32 }}>Loading analytics showcase...</div>;
  if (error) return <div style={{ maxWidth: 1200, margin: "0 auto", padding: 32 }}>Failed to load analytics data.</div>;
  if (!customerChurn) return <div style={{ maxWidth: 1200, margin: "0 auto", padding: 32 }}>Failed to load analytics data.</div>;

  return (
    <main
      style={{
        maxWidth: 1200,
        margin: "0 auto",
        padding: "24px 32px 40px",
        display: "grid",
        gap: 46,
      }}
    >
      <header
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          flexWrap: "wrap",
          gap: 16,
          padding: 24,
          background: "#fff",
          border: "1px solid #e5e7eb",
          borderRadius: 12,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <img
            style={{
              width: 64,
              height: 64,
              borderRadius: 12,
              objectFit: "cover",
              flexShrink: 0,
            }}
            src="/showcase-mark.jpg"
            alt="Commerce Analytics Showcase mark"
          />
          <div>
            <p
              style={{
                margin: 0,
                fontSize: 12,
                letterSpacing: 2,
                textTransform: "uppercase",
                color: "#6b7280",
              }}
            >
              Open Source Portfolio
            </p>
            <h1 style={{ margin: "6px 0 8px", fontSize: 32 }}>Commerce Analytics Showcase</h1>
            <p style={{ margin: 0, color: "#4b5563", lineHeight: 1.5 }}>
              A Power BI-inspired dashboard built to showcase React, Node.js, and retail analytics modeling in one project.
            </p>
          </div>
        </div>
      </header>

      <CustomerChurnCard data={customerChurn} />

      <div
        style={{
          display: "grid",
          gap: 24,
          gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
        }}
      >
        <RevenueChart data={revenue} />
        <TurnoverChart data={turnoverByCategory} />
      </div>

      <div
        style={{
          display: "grid",
          gap: 24,
          gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
        }}
      >
        <TopProductsChart data={topProducts} />
        <InventorySignals lowStockHighSales={lowStockHighSales} />
      </div>
    </main>
  );
}
