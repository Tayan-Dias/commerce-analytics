interface FiltersProps {
  label: string;
  options: string[];
  value: string;
  onChange: (value: string) => void;
}

export default function Filters({ label, options, value, onChange }: FiltersProps) {
  return (
    <label
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 8,
        minWidth: 180,
        fontSize: 14,
        color: "#4b5563",
      }}
    >
      <span style={{ fontWeight: 600 }}>{label}</span>
      <select
        style={{
          padding: "10px 12px",
          border: "1px solid #d1d5db",
          borderRadius: 8,
          background: "#fff",
          color: "#1f2937",
          font: "inherit",
        }}
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        <option value="All">All</option>
        {options.map((option) => (
          <option key={option} value={option}>{option}</option>
        ))}
      </select>
    </label>
  );
}
