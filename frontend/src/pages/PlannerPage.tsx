import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import {
  getItineraries,
  createItinerary,
  deleteItinerary,
  addStop,
  deleteStop,
} from "../api/itineraries";
import apiClient from "../api/client";

type Stop = {
  id: string;
  destination_id: string;
  destination_name: string;
  day_number: number;
  order: number;
  notes: string;
};

type Itinerary = {
  id: string;
  title: string;
  start_date: string;
  end_date: string;
  stops: Stop[];
};

type Destination = {
  id: string;
  name: string;
  country: string;
};

const s = {
  card: {
    background: "white",
    borderRadius: "14px",
    padding: "18px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.06)",
    border: "1px solid #e5e7eb",
  } as React.CSSProperties,
  input: {
    width: "100%",
    padding: "10px 12px",
    borderRadius: "8px",
    border: "1px solid #d1d5db",
    fontSize: "14px",
    boxSizing: "border-box" as const,
    outline: "none",
  } as React.CSSProperties,
  btnPrimary: {
    background: "#14b8a6",
    color: "white",
    border: "none",
    padding: "10px 18px",
    borderRadius: "8px",
    fontWeight: 600,
    cursor: "pointer",
    fontSize: "14px",
  } as React.CSSProperties,
  btnGhost: {
    background: "#e5e7eb",
    color: "#374151",
    border: "none",
    padding: "10px 18px",
    borderRadius: "8px",
    fontWeight: 600,
    cursor: "pointer",
    fontSize: "14px",
  } as React.CSSProperties,
  btnDanger: {
    background: "#fee2e2",
    color: "#dc2626",
    border: "none",
    padding: "6px 10px",
    borderRadius: "6px",
    cursor: "pointer",
    fontSize: "13px",
    fontWeight: 500,
  } as React.CSSProperties,
};

function PlannerPage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [itineraries, setItineraries] = useState<Itinerary[]>([]);
  const [selected, setSelected] = useState<Itinerary | null>(null);
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // New itinerary form
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [title, setTitle] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  // Add stop form
  const [showStopForm, setShowStopForm] = useState(false);
  const [selectedDestId, setSelectedDestId] = useState("");
  const [dayNumber, setDayNumber] = useState(1);
  const [stopNotes, setStopNotes] = useState("");

  useEffect(() => {
    if (!user) {
      navigate("/login?next=/planner");
      return;
    }
    Promise.all([fetchItineraries(), fetchDestinations()]).finally(() =>
      setLoading(false),
    );
  }, [user]);

  async function fetchItineraries() {
    try {
      const data = await getItineraries();
      setItineraries(data.map((it: any) => ({ ...it, stops: it.stops ?? [] })));
    } catch {
      setError("Could not load itineraries.");
    }
  }

  async function fetchDestinations() {
    try {
      const res = await apiClient.get("/destinations?limit=100");
      setDestinations(res.data);
    } catch {}
  }

  async function handleCreate() {
    if (!title.trim() || !startDate || !endDate) {
      setError("Please fill in all fields.");
      return;
    }
    setError("");
    try {
      const created = await createItinerary({
        title: title.trim(),
        start_date: startDate,
        end_date: endDate,
        is_public: false,
      });
      const newIt = { ...created, stops: [] };
      setItineraries((prev) => [...prev, newIt]);
      setSelected(newIt);
      setShowCreateForm(false);
      setTitle("");
      setStartDate("");
      setEndDate("");
    } catch {
      setError("Could not create itinerary.");
    }
  }

  async function handleDeleteItinerary(id: string) {
    try {
      await deleteItinerary(id);
      setItineraries((prev) => prev.filter((it) => it.id !== id));
      if (selected?.id === id) setSelected(null);
    } catch {
      setError("Could not delete itinerary.");
    }
  }

  async function handleAddStop() {
    if (!selected || !selectedDestId) {
      setError("Please select a destination.");
      return;
    }
    setError("");
    try {
      const newStop = await addStop(selected.id, {
        destination_id: selectedDestId,
        day_number: dayNumber,
        order: selected.stops.length + 1,
        notes: stopNotes,
      });
      const updatedStops = [...selected.stops, newStop];
      setSelected((prev) => (prev ? { ...prev, stops: updatedStops } : prev));
      setItineraries((prev) =>
        prev.map((it) =>
          it.id === selected.id ? { ...it, stops: updatedStops } : it,
        ),
      );
      setSelectedDestId("");
      setStopNotes("");
      setShowStopForm(false);
    } catch {
      setError("Could not add stop.");
    }
  }

  async function handleDeleteStop(stopId: string) {
    if (!selected) return;
    try {
      await deleteStop(selected.id, stopId);
      const updatedStops = selected.stops.filter((s) => s.id !== stopId);
      setSelected((prev) => (prev ? { ...prev, stops: updatedStops } : prev));
      setItineraries((prev) =>
        prev.map((it) =>
          it.id === selected.id ? { ...it, stops: updatedStops } : it,
        ),
      );
    } catch {
      setError("Could not remove stop.");
    }
  }

  if (loading) {
    return (
      <div style={{ padding: "60px", textAlign: "center", color: "#6b7280" }}>
        Loading your plans...
      </div>
    );
  }

  return (
    <div style={{ padding: "40px", maxWidth: "1100px", margin: "0 auto" }}>
      {/* Header */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "28px",
        }}
      >
        <div>
          <h1 style={{ fontSize: "32px", marginBottom: "6px", color: "#1f2937" }}>
            Trip Planner
          </h1>
          <p style={{ color: "#6b7280" }}>
            Create and manage your travel itineraries.
          </p>
        </div>
        <button style={s.btnPrimary} onClick={() => setShowCreateForm(!showCreateForm)}>
          + New Plan
        </button>
      </div>

      {/* Error */}
      {error && (
        <div
          style={{
            background: "#fee2e2",
            color: "#dc2626",
            padding: "12px 16px",
            borderRadius: "8px",
            marginBottom: "16px",
            fontSize: "14px",
          }}
        >
          {error}
        </div>
      )}

      {/* Create form */}
      {showCreateForm && (
        <div style={{ ...s.card, marginBottom: "24px" }}>
          <h2 style={{ fontSize: "18px", marginBottom: "16px" }}>New Itinerary</h2>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr 1fr",
              gap: "12px",
              marginBottom: "14px",
            }}
          >
            <div>
              <label style={{ display: "block", marginBottom: "6px", fontSize: "13px", fontWeight: 600 }}>
                Title
              </label>
              <input
                style={s.input}
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Turkey Summer 2025"
              />
            </div>
            <div>
              <label style={{ display: "block", marginBottom: "6px", fontSize: "13px", fontWeight: 600 }}>
                Start Date
              </label>
              <input
                style={s.input}
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>
            <div>
              <label style={{ display: "block", marginBottom: "6px", fontSize: "13px", fontWeight: 600 }}>
                End Date
              </label>
              <input
                style={s.input}
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
          </div>
          <div style={{ display: "flex", gap: "8px" }}>
            <button style={s.btnPrimary} onClick={handleCreate}>
              Create
            </button>
            <button style={s.btnGhost} onClick={() => setShowCreateForm(false)}>
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Two-column layout */}
      <div style={{ display: "grid", gridTemplateColumns: "260px 1fr", gap: "24px" }}>
        {/* Plans list */}
        <div>
          <h2
            style={{
              fontSize: "15px",
              fontWeight: 700,
              marginBottom: "12px",
              color: "#374151",
              textTransform: "uppercase",
              letterSpacing: "0.05em",
            }}
          >
            My Plans
          </h2>
          {itineraries.length === 0 ? (
            <div
              style={{
                ...s.card,
                textAlign: "center",
                color: "#9ca3af",
                fontSize: "14px",
                padding: "30px",
              }}
            >
              No plans yet.
              <br />
              Create one to get started!
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              {itineraries.map((it) => (
                <div
                  key={it.id}
                  style={{
                    ...s.card,
                    cursor: "pointer",
                    borderColor: selected?.id === it.id ? "#14b8a6" : "#e5e7eb",
                    borderWidth: "2px",
                  }}
                  onClick={() => setSelected(it)}
                >
                  <div style={{ fontWeight: 600, fontSize: "14px", marginBottom: "4px" }}>
                    {it.title}
                  </div>
                  <div style={{ fontSize: "12px", color: "#6b7280" }}>
                    {it.start_date} → {it.end_date}
                  </div>
                  <div style={{ fontSize: "12px", color: "#9ca3af", marginTop: "2px" }}>
                    {it.stops?.length ?? 0} stop{it.stops?.length !== 1 ? "s" : ""}
                  </div>
                  <button
                    style={{ ...s.btnDanger, marginTop: "8px", fontSize: "12px" }}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteItinerary(it.id);
                    }}
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Plan detail */}
        <div>
          {!selected ? (
            <div
              style={{
                ...s.card,
                textAlign: "center",
                color: "#9ca3af",
                padding: "60px",
                fontSize: "15px",
              }}
            >
              Select a plan from the left to manage its stops.
            </div>
          ) : (
            <>
              {/* Plan header */}
              <div style={{ ...s.card, marginBottom: "16px" }}>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-start",
                    marginBottom: "16px",
                  }}
                >
                  <div>
                    <h2 style={{ fontSize: "22px", fontWeight: 700, margin: 0 }}>
                      {selected.title}
                    </h2>
                    <p style={{ color: "#6b7280", fontSize: "14px", margin: "4px 0 0" }}>
                      {selected.start_date} → {selected.end_date}
                    </p>
                  </div>
                  <Link
                    to={`/planner/${selected.id}/budget`}
                    style={{
                      background: "#0f766e",
                      color: "white",
                      textDecoration: "none",
                      padding: "10px 16px",
                      borderRadius: "8px",
                      fontWeight: 600,
                      fontSize: "14px",
                    }}
                  >
                    Budget Planner
                  </Link>
                </div>

                {/* Stops */}
                {selected.stops.length === 0 ? (
                  <p style={{ color: "#9ca3af", fontSize: "14px" }}>
                    No stops yet. Add your first destination!
                  </p>
                ) : (
                  <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                    {selected.stops.map((stop) => (
                      <div
                        key={stop.id}
                        style={{
                          padding: "12px 16px",
                          borderRadius: "10px",
                          background: "#f8fafc",
                          border: "1px solid #e5e7eb",
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                        }}
                      >
                        <div>
                          <span
                            style={{
                              fontWeight: 700,
                              color: "#14b8a6",
                              marginRight: "8px",
                              fontSize: "13px",
                            }}
                          >
                            Day {stop.day_number}
                          </span>
                          <span style={{ fontWeight: 600 }}>{stop.destination_name}</span>
                          {stop.notes && (
                            <p style={{ margin: "4px 0 0", fontSize: "13px", color: "#6b7280" }}>
                              {stop.notes}
                            </p>
                          )}
                        </div>
                        <button
                          style={s.btnDanger}
                          onClick={() => handleDeleteStop(stop.id)}
                        >
                          ✕
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Add stop */}
              {showStopForm ? (
                <div style={s.card}>
                  <h3 style={{ fontSize: "16px", marginBottom: "14px" }}>Add a Stop</h3>
                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns: "1fr 1fr",
                      gap: "12px",
                      marginBottom: "12px",
                    }}
                  >
                    <div>
                      <label
                        style={{
                          display: "block",
                          marginBottom: "6px",
                          fontSize: "13px",
                          fontWeight: 600,
                        }}
                      >
                        Destination
                      </label>
                      <select
                        style={s.input}
                        value={selectedDestId}
                        onChange={(e) => setSelectedDestId(e.target.value)}
                      >
                        <option value="">Select city...</option>
                        {destinations.map((d) => (
                          <option key={d.id} value={d.id}>
                            {d.name}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label
                        style={{
                          display: "block",
                          marginBottom: "6px",
                          fontSize: "13px",
                          fontWeight: 600,
                        }}
                      >
                        Day Number
                      </label>
                      <input
                        style={s.input}
                        type="number"
                        min={1}
                        value={dayNumber}
                        onChange={(e) => setDayNumber(Number(e.target.value))}
                      />
                    </div>
                  </div>
                  <div style={{ marginBottom: "12px" }}>
                    <label
                      style={{
                        display: "block",
                        marginBottom: "6px",
                        fontSize: "13px",
                        fontWeight: 600,
                      }}
                    >
                      Notes (optional)
                    </label>
                    <input
                      style={s.input}
                      value={stopNotes}
                      onChange={(e) => setStopNotes(e.target.value)}
                      placeholder="e.g. Arrive by train, check in early"
                    />
                  </div>
                  <div style={{ display: "flex", gap: "8px" }}>
                    <button style={s.btnPrimary} onClick={handleAddStop}>
                      Add Stop
                    </button>
                    <button
                      style={s.btnGhost}
                      onClick={() => setShowStopForm(false)}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <button style={s.btnPrimary} onClick={() => setShowStopForm(true)}>
                  + Add Stop
                </button>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default PlannerPage;
