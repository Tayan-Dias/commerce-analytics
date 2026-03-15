interface FiltersProps {
  categories: string[];
  value: string;
  onChange: (value: string) => void;
}

export default function Filters({ categories, value, onChange }: FiltersProps) {
  return (
    <label
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 8,
        minWidth: 180,
        fontSize: 14,
        color: "#4b5563"
      }}
    >
      <span style={{ fontWeight: 600 }}>Category Filter</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        style={{
          padding: "10px 12px",
          borderRadius: 8,
          border: "1px solid #d1d5db",
          background: "#fff",
          color: "#1f2937"
        }}
      >
        <option value="All">All</option>
        {categories.map((category) => (
          <option key={category} value={category}>{category}</option>
        ))}
      </select>
    </label>
  );
}
