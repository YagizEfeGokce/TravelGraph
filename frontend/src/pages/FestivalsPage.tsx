import { useState, useEffect, useMemo } from "react";
import { getFestivals } from "../api/festivals";

type Festival = {
  id: string;
  name: string;
  description: string;
  start_date: string;
  end_date: string;
  city: string;
  ticket_price?: number;
  is_recurring?: boolean;
};

const TODAY = new Date().toISOString().split("T")[0];

function addMonths(months: number): string {
  const d = new Date();
  d.setMonth(d.getMonth() + months);
  return d.toISOString().split("T")[0];
}

function FestivalsPage() {
  const [festivals, setFestivals] = useState<Festival[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [searchText, setSearchText] = useState("");
  const [selectedCity, setSelectedCity] = useState("All");
  const [timeFilter, setTimeFilter] = useState<"all" | "upcoming" | "3months" | "year">("all");

  useEffect(() => {
    getFestivals()
      .then(setFestivals)
      .catch(() => setError("Could not load festivals."))
      .finally(() => setLoading(false));
  }, []);

  const cities = useMemo(() => {
    const unique = Array.from(new Set(festivals.map((f) => f.city))).sort();
    return unique;
  }, [festivals]);

  const filtered = useMemo(() => {
    let list = festivals;

    if (selectedCity !== "All") {
      list = list.filter((f) => f.city === selectedCity);
    }

    if (searchText.trim()) {
      const q = searchText.toLowerCase();
      list = list.filter(
        (f) =>
          f.name.toLowerCase().includes(q) ||
          f.city.toLowerCase().includes(q) ||
          f.description.toLowerCase().includes(q),
      );
    }

    if (timeFilter === "upcoming") {
      list = list.filter((f) => f.end_date >= TODAY);
    } else if (timeFilter === "3months") {
      const cutoff = addMonths(3);
      list = list.filter((f) => f.start_date >= TODAY && f.start_date <= cutoff);
    } else if (timeFilter === "year") {
      const cutoff = addMonths(12);
      list = list.filter((f) => f.start_date >= TODAY && f.start_date <= cutoff);
    }

    return list;
  }, [festivals, selectedCity, searchText, timeFilter]);

  const inputStyle: React.CSSProperties = {
    padding: "11px 14px",
    border: "1px solid #d1d5db",
    borderRadius: "10px",
    fontSize: "14px",
    outline: "none",
  };

  const chipBtn = (active: boolean): React.CSSProperties => ({
    padding: "8px 14px",
    borderRadius: "8px",
    border: "1px solid",
    borderColor: active ? "#14b8a6" : "#d1d5db",
    background: active ? "#f0fafa" : "white",
    color: active ? "#0f766e" : "#6b7280",
    fontWeight: active ? 700 : 500,
    cursor: "pointer",
    fontSize: "13px",
  });

  return (
    <div style={{ padding: "40px", maxWidth: "1200px", margin: "0 auto" }}>
      {/* Header */}
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ fontSize: "36px", marginBottom: "10px", color: "#1f2937" }}>
          Festival Calendar
        </h1>
        <p style={{ color: "#6b7280" }}>
          Discover festivals and cultural events across Turkey.
        </p>
      </div>

      {/* Filters */}
      <div
        style={{
          background: "white",
          padding: "18px",
          borderRadius: "16px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.06)",
          marginBottom: "28px",
          display: "flex",
          gap: "12px",
          flexWrap: "wrap",
          alignItems: "center",
        }}
      >
        <input
          type="text"
          placeholder="Search festivals or cities..."
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          style={{ ...inputStyle, flex: "1 1 220px" }}
        />

        <select
          value={selectedCity}
          onChange={(e) => setSelectedCity(e.target.value)}
          style={{ ...inputStyle, minWidth: "180px" }}
        >
          <option value="All">All Cities</option>
          {cities.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>

        <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
          {(
            [
              ["all", "All"],
              ["upcoming", "Upcoming"],
              ["3months", "Next 3 months"],
              ["year", "This year"],
            ] as const
          ).map(([val, label]) => (
            <button
              key={val}
              style={chipBtn(timeFilter === val)}
              onClick={() => setTimeFilter(val)}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Result count */}
      <p style={{ color: "#6b7280", fontSize: "14px", marginBottom: "16px" }}>
        {loading ? "Loading..." : `${filtered.length} festival${filtered.length !== 1 ? "s" : ""} found`}
      </p>

      {error && (
        <div style={{ color: "#dc2626", marginBottom: "16px", fontSize: "14px" }}>
          {error}
        </div>
      )}

      {/* Grid */}
      {!loading && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
            gap: "20px",
          }}
        >
          {filtered.length === 0 ? (
            <p style={{ color: "#9ca3af", gridColumn: "1/-1", textAlign: "center", padding: "40px" }}>
              No festivals match your filters.
            </p>
          ) : (
            filtered.map((festival) => (
              <div
                key={festival.id}
                style={{
                  background: "white",
                  borderRadius: "16px",
                  padding: "20px",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.06)",
                  border: "1px solid #e5e7eb",
                }}
              >
                <div
                  style={{
                    display: "inline-block",
                    background: "#f0fafa",
                    color: "#0f766e",
                    padding: "4px 10px",
                    borderRadius: "6px",
                    fontSize: "12px",
                    fontWeight: 700,
                    marginBottom: "10px",
                  }}
                >
                  {festival.city}
                </div>
                <h3
                  style={{
                    fontSize: "16px",
                    fontWeight: 700,
                    marginBottom: "8px",
                    color: "#1f2937",
                  }}
                >
                  {festival.name}
                </h3>
                <p
                  style={{
                    fontSize: "13px",
                    color: "#6b7280",
                    marginBottom: "12px",
                    lineHeight: 1.5,
                  }}
                >
                  {festival.description}
                </p>
                <p style={{ fontSize: "13px", color: "#374151", marginBottom: "4px" }}>
                  📅 {festival.start_date}
                  {festival.end_date !== festival.start_date && ` → ${festival.end_date}`}
                </p>
                {festival.ticket_price != null && (
                  <p style={{ fontSize: "13px", color: "#374151" }}>
                    🎟 {festival.ticket_price === 0 ? "Free entry" : `₺${festival.ticket_price}`}
                  </p>
                )}
                {festival.is_recurring && (
                  <span
                    style={{
                      display: "inline-block",
                      marginTop: "8px",
                      fontSize: "11px",
                      color: "#6b7280",
                      background: "#f3f4f6",
                      padding: "2px 8px",
                      borderRadius: "4px",
                    }}
                  >
                    Annual event
                  </span>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default FestivalsPage;
