import { Link } from "react-router-dom";

function PlannerPage() {
  const stops = [
    "Arrival at city center",
    "Museum visit",
    "Lunch at local restaurant",
    "Evening walking tour",
  ];

  return (
    <div style={{ padding: "40px", maxWidth: "1100px", margin: "0 auto" }}>
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ fontSize: "36px", marginBottom: "10px", color: "#1f2937" }}>
          Route Planner
        </h1>
        <p style={{ color: "#6b7280" }}>
          Organize your itinerary and arrange your trip stops in the best order.
        </p>
      </div>

      <div
        style={{
          background: "white",
          borderRadius: "18px",
          padding: "24px",
          boxShadow: "0 8px 18px rgba(0,0,0,0.06)",
          marginBottom: "24px",
        }}
      >
        <h2 style={{ marginBottom: "16px" }}>Your Itinerary</h2>

        <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
          {stops.map((stop, index) => (
            <div
              key={stop}
              style={{
                padding: "16px",
                borderRadius: "12px",
                border: "1px solid #e5e7eb",
                background: "#f8fafc",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <span>
                {index + 1}. {stop}
              </span>
              <span style={{ color: "#14b8a6", fontWeight: 600 }}>Drag</span>
            </div>
          ))}
        </div>
      </div>

      <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
        <button
          style={{
            background: "#14b8a6",
            color: "white",
            border: "none",
            padding: "12px 18px",
            borderRadius: "10px",
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          Add Stop
        </button>

        <button
          style={{
            background: "white",
            color: "#1f2937",
            border: "1px solid #d1d5db",
            padding: "12px 18px",
            borderRadius: "10px",
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          Save Plan
        </button>

        <Link
          to="/planner/demo-trip/budget"
          style={{
            background: "#0f766e",
            color: "white",
            textDecoration: "none",
            padding: "12px 18px",
            borderRadius: "10px",
            fontWeight: 600,
            display: "inline-block",
          }}
        >
          Go to Budget Planner
        </Link>
      </div>
    </div>
  );
}

export default PlannerPage;