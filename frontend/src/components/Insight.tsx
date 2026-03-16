export default function Insight({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ marginTop: 16 }}>
      <hr
        style={{
          margin: "0 0 12px",
          border: 0,
          borderTop: "1px solid #e5e7eb",
        }}
      />
      <p
        style={{
          margin: 0,
          padding: 12,
          background: "#f8fafc",
          border: "1px solid #e5e7eb",
          borderRadius: 10,
          color: "#4b5563",
          lineHeight: 1.5,
        }}
      >
        <strong>Insight:</strong> {children}
      </p>
    </div>
  );
}
