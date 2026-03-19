import { useMemo, useState } from "react";

function BudgetPlannerPage() {
  const [accommodation, setAccommodation] = useState(120);
  const [food, setFood] = useState(80);
  const [transport, setTransport] = useState(50);
  const [activities, setActivities] = useState(70);

  const total = useMemo(() => {
    return accommodation + food + transport + activities;
  }, [accommodation, food, transport, activities]);

  return (
    <div
      style={{
        maxWidth: "900px",
        margin: "0 auto",
        padding: "40px 20px",
      }}
    >
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ fontSize: "36px", marginBottom: "10px", color: "#1f2937" }}>
          Budget Planner
        </h1>
        <p style={{ color: "#6b7280" }}>
          Add your travel expenses item by item and track the total budget.
        </p>
      </div>

      <div
        style={{
          background: "white",
          borderRadius: "18px",
          padding: "24px",
          boxShadow: "0 8px 18px rgba(0,0,0,0.06)",
          display: "grid",
          gap: "18px",
        }}
      >
        <BudgetField
          label="Accommodation"
          value={accommodation}
          onChange={setAccommodation}
        />
        <BudgetField label="Food" value={food} onChange={setFood} />
        <BudgetField
          label="Transport"
          value={transport}
          onChange={setTransport}
        />
        <BudgetField
          label="Activities"
          value={activities}
          onChange={setActivities}
        />

        <div
          style={{
            marginTop: "12px",
            paddingTop: "18px",
            borderTop: "1px solid #e5e7eb",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <h2 style={{ margin: 0 }}>Total</h2>
          <span
            style={{
              fontSize: "24px",
              fontWeight: 700,
              color: "#14b8a6",
            }}
          >
            €{total}
          </span>
        </div>

        <button
          style={{
            background: "#14b8a6",
            color: "white",
            border: "none",
            padding: "14px 18px",
            borderRadius: "10px",
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          Save Budget
        </button>
      </div>
    </div>
  );
}

type BudgetFieldProps = {
  label: string;
  value: number;
  onChange: (value: number) => void;
};

function BudgetField({ label, value, onChange }: BudgetFieldProps) {
  return (
    <div>
      <label
        style={{
          display: "block",
          marginBottom: "8px",
          fontWeight: 600,
          color: "#374151",
        }}
      >
        {label}
      </label>
      <input
        type="number"
        min="0"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        style={{
          width: "100%",
          padding: "14px 16px",
          borderRadius: "10px",
          border: "1px solid #d1d5db",
          fontSize: "15px",
          boxSizing: "border-box",
        }}
      />
    </div>
  );
}

export default BudgetPlannerPage;