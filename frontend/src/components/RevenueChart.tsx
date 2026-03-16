import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import Insight from "./Insight";
import type { RevenueItem } from "../types/metrics";

function formatCurrency(value: number) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

function formatCompactCurrency(value: number) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value);
}

export default function RevenueChart({ data }: { data: RevenueItem[] }) {
  const totalRevenue = data.reduce((sum, item) => sum + item.revenue, 0);
  let topRegion = data[0];

  for (const item of data) {
    if (item.revenue > topRegion.revenue) {
      topRegion = item;
    }
  }

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
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ margin: "0 0 6px", fontSize: 22 }}>Revenue by Region</h2>
        <p style={{ margin: 0, color: "#6b7280", lineHeight: 1.5 }}>
          Compare the sales contribution of each region in USD.
        </p>
      </div>
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data}>
          <XAxis dataKey="region" />
          <YAxis tickFormatter={formatCompactCurrency} />
          <Tooltip formatter={(value) => formatCurrency(Number(value))} />
          <Bar dataKey="revenue" fill="#2d6cdf" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <Insight>
        {topRegion.region} leads regional revenue with {formatCurrency(topRegion.revenue)},
        representing {((topRegion.revenue / totalRevenue) * 100).toFixed(1)}% of the total.
      </Insight>
    </section>
  );
}
