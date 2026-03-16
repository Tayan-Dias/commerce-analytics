import { useState } from "react";

import Filters from "./Filters";
import Insight from "./Insight";
import type { StockMetric } from "../types/metrics";

function SignalCard({ item }: { item: StockMetric }) {
  return (
    <div
      style={{
        background: "#f8fafc",
        border: "1px solid #e5e7eb",
        borderRadius: 10,
        padding: 12,
      }}
    >
      <strong style={{ display: "block", color: "#111827" }}>
        Product #{item.product_id} - {item.category}
      </strong>
      <p style={{ margin: "8px 0 0", color: "#4b5563" }}>
        Stock: {item.current_stock} - Sold: {item.total_quantity_sold}
      </p>
    </div>
  );
}

export default function InventorySignals({
  lowStockHighSales,
}: {
  lowStockHighSales: StockMetric[];
}) {
  const categoryOptions = [...new Set(lowStockHighSales.map((item) => item.category))];
  const [selectedCategory, setSelectedCategory] = useState("All");

  let filteredLowStock = lowStockHighSales;

  if (selectedCategory !== "All") {
    filteredLowStock = lowStockHighSales.filter((item) => item.category === selectedCategory);
  }

  let strongestLowStockRisk = filteredLowStock[0];

  for (const item of filteredLowStock) {
    if (strongestLowStockRisk && item.total_quantity_sold > strongestLowStockRisk.total_quantity_sold) {
      strongestLowStockRisk = item;
    }
  }

  return (
    <section
      style={{
        background: "#fff",
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 16,
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
          <h2 style={{ margin: "0 0 6px", fontSize: 22 }}>Inventory Signals</h2>
          <p style={{ margin: 0, color: "#6b7280", lineHeight: 1.5 }}>
            Spot products with strong sales and low stock.
          </p>
        </div>
        <div style={{ minWidth: 220 }}>
          <Filters
            label="Category Filter"
            options={categoryOptions}
            value={selectedCategory}
            onChange={setSelectedCategory}
          />
        </div>
      </div>
      <div
        style={{
          display: "grid",
          gap: 12,
        }}
      >
        {!filteredLowStock.length && (
          <p style={{ margin: 0, color: "#6b7280" }}>
            No low-stock products match the current filter.
          </p>
        )}
        {filteredLowStock.map((item) => (
          <SignalCard key={`${item.product_id}-${item.category}`} item={item} />
        ))}
      </div>
      {!!strongestLowStockRisk && (
        <Insight>
          Product #{strongestLowStockRisk.product_id} in{" "}
          {strongestLowStockRisk.category} is the strongest restocking signal, with{" "}
          {strongestLowStockRisk.total_quantity_sold} units sold and only{" "}
          {strongestLowStockRisk.current_stock} in stock.
        </Insight>
      )}
    </section>
  );
}
