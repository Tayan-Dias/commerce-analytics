import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import type { RevenueItem } from "../types/metrics";

export default function RevenueChart({ data }: { data: RevenueItem[] }) {
  return (
    <div style={{ background: "#fff", padding: 16, borderRadius: 12, marginBottom: 24 }}>
      <h2>Revenue by Region</h2>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data}>
          <XAxis dataKey="region" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="revenue" fill="#2d6cdf" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
