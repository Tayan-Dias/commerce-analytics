import { useState } from "react";
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import Filters from "./Filters";
import Insight from "./Insight";
import type { TopProduct } from "../types/metrics";

export default function TopProductsChart({ data }: { data: TopProduct[] }) {
  const categories = [...new Set(data.map((item) => item.category))];
  const [selectedCategory, setSelectedCategory] = useState("All");
  let filteredProducts = data;

  if (selectedCategory !== "All") {
    filteredProducts = data.filter((item) => item.category === selectedCategory);
  }

  const chartData = filteredProducts.slice(0, 10).map((item) => ({
    ...item,
    label: `#${item.product_id} ${item.category}`
  }));
  const topProduct = filteredProducts[0];

  return (
    <section
      style={{
        background: "#fff",
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 16,
        height: "100%",
      }}
    >
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "minmax(0, 7fr) minmax(220px, 3fr)",
          alignItems: "start",
          gap: 16,
          marginBottom: 16,
        }}
      >
        <div style={{ minWidth: 0 }}>
          <h2 style={{ margin: "0 0 6px", fontSize: 22 }}>Top Selling Products</h2>
          <p style={{ margin: 0, color: "#6b7280", lineHeight: 1.5 }}>
            Ranked by quantity sold, with an optional category filter.
          </p>
        </div>
        <div style={{ minWidth: 220 }}>
          <Filters
            label="Category Filter"
            options={categories}
            value={selectedCategory}
            onChange={setSelectedCategory}
          />
        </div>
      </div>
      <ResponsiveContainer width="100%" height={340}>
        <BarChart data={chartData} layout="vertical">
          <XAxis type="number" />
          <YAxis type="category" dataKey="label" width={120} />
          <Tooltip />
          <Bar dataKey="total_quantity_sold" fill="#1f9d74" radius={[0, 6, 6, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <Insight>
        Product #{topProduct.product_id} leads the current view with{" "}
        {topProduct.total_quantity_sold} units sold in {topProduct.category}.
      </Insight>
    </section>
  );
}
