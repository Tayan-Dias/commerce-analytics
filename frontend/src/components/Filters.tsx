interface FiltersProps {
  categories: string[];
  value: string;
  onChange: (value: string) => void;
}

export default function Filters({ categories, value, onChange }: FiltersProps) {
  return (
    <label style={{ display: "block", marginBottom: 24 }}>
      Category Filter{" "}
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        <option value="All">All</option>
        {categories.map((category) => (
          <option key={category} value={category}>{category}</option>
        ))}
      </select>
    </label>
  );
}
