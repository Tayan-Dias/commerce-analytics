import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import Insight from "./Insight";
import type { CategoryTurnover } from "../types/metrics";

function formatTurnover(value: number) {
  return `${value.toFixed(1)}x`;
}

export default function TurnoverChart({ data }: { data: CategoryTurnover[] }) {
  const highestTurnover = data[0];
  const lowestTurnover = data[data.length - 1];

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
      <h2 style={{ margin: "0 0 6px", fontSize: 22 }}>Turnover by Category</h2>
      <p style={{ margin: "0 0 16px", color: "#6b7280", lineHeight: 1.5 }}>
        Turnover = sold quantity / current stock. Higher means faster movement.
      </p>
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data}>
          <XAxis dataKey="category" />
          <YAxis tickFormatter={formatTurnover} />
          <Tooltip formatter={(value) => formatTurnover(Number(value))} />
          <Bar dataKey="turnover_rate" fill="#d97706" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <Insight>
        {highestTurnover.category} has the fastest stock movement at{" "}
        {highestTurnover.turnover_rate.toFixed(2)}x, while {lowestTurnover.category} is the
        slowest at {lowestTurnover.turnover_rate.toFixed(2)}x.
      </Insight>
    </section>
  );
}
