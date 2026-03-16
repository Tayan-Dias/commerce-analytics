import Insight from "./Insight";
import type { CustomerChurn } from "../types/metrics";

export default function CustomerChurnCard({ data }: { data: CustomerChurn }) {
  const stats = [
    { label: "Total Customers", value: String(data.total_customers) },
    { label: "Active Customers", value: String(data.active_customers) },
    { label: "Churned Customers", value: String(data.churned_customers) },
    { label: "Churn Rate", value: `${(data.churn_rate * 100).toFixed(1)}%` },
  ];

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
      <h2 style={{ margin: "0 0 6px", fontSize: 22 }}>Customer Churn</h2>
      <p style={{ margin: "0 0 16px", color: "#6b7280", lineHeight: 1.5 }}>
        Customers without purchases in the last 90 days.
      </p>
      <div
        style={{
          display: "grid",
          gap: 12,
          gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
        }}
      >
        {stats.map((stat) => (
          <div
            key={stat.label}
            style={{
              background: "#f8fafc",
              border: "1px solid #e5e7eb",
              borderRadius: 10,
              padding: 16,
            }}
          >
            <p style={{ margin: "0 0 8px", fontSize: 14, color: "#6b7280" }}>{stat.label}</p>
            <strong style={{ fontSize: 28, color: "#111827" }}>{stat.value}</strong>
          </div>
        ))}
      </div>
      <Insight>
        {data.churned_customers} of {data.total_customers} customers are currently churned,
        a rate of {(data.churn_rate * 100).toFixed(1)}%.
      </Insight>
    </section>
  );
}
