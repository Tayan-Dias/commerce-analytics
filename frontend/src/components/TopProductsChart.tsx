import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import type { TopProduct } from "../types/metrics";

export default function TopProductsChart({ data }: { data: TopProduct[] }) {
  const chartData = data.slice(0, 10).map((item) => ({
    ...item,
    label: `#${item.product_id} ${item.category}`
  }));

  return (
    <div style={{ background: "#fff", padding: 16, borderRadius: 12 }}>
      <h2>Top Selling Products</h2>
      <ResponsiveContainer width="100%" height={340}>
        <BarChart data={chartData} layout="vertical">
          <XAxis type="number" />
          <YAxis type="category" dataKey="label" width={120} />
          <Tooltip />
          <Bar dataKey="total_quantity_sold" fill="#1f9d74" radius={[0, 6, 6, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
