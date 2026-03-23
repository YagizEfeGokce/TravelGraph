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
  image_url?: string;
};

const CANVAS_W = 860;
const CANVAS_H = 460;

function computeNodePositions(count: number) {
  if (count === 0) return [];
  if (count === 1) return [{ x: CANVAS_W / 2 - 30, y: CANVAS_H / 2 - 30 }];
  const R = Math.min(CANVAS_W, CANVAS_H) * 0.32;
  const cx = CANVAS_W / 2;
  const cy = CANVAS_H / 2;
  return Array.from({ length: count }, (_, i) => {
    const angle = (i * 2 * Math.PI) / count - Math.PI / 2;
    return { x: cx + R * Math.cos(angle) - 30, y: cy + R * Math.sin(angle) - 30 };
  });
}

const NAV_ITEMS = [
  { key: "home", icon: "home", label: "Home", to: "/" },
  { key: "graphs", icon: "route", label: "My Graphs", to: null },
  { key: "budget", icon: "account_balance_wallet", label: "Budget", to: null },
  { key: "settings", icon: "settings", label: "Settings", to: "/profile" },
] as const;

function PlannerPage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [itineraries, setItineraries] = useState<Itinerary[]>([]);
  const [selected, setSelected] = useState<Itinerary | null>(null);
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeNav, setActiveNav] = useState<string>("graphs");

  // Create form
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [title, setTitle] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  // Add stop form
  const [showStopForm, setShowStopForm] = useState(false);
  const [selectedDestId, setSelectedDestId] = useState("");
  const [dayNumber, setDayNumber] = useState(1);
  const [stopNotes, setStopNotes] = useState("");

  // Suggested next destination (not yet in plan)
  const suggestedDest = destinations.find(
    (d) => !selected?.stops.some((s) => s.destination_id === d.id),
  );

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

  async function handleAddStop(destId?: string) {
    const targetDestId = destId ?? selectedDestId;
    if (!selected || !targetDestId) {
      setError("Please select a destination.");
      return;
    }
    setError("");
    try {
      const newStop = await addStop(selected.id, {
        destination_id: targetDestId,
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

  const nodePositions = computeNodePositions(selected?.stops.length ?? 0);
  const tripDays = selected
    ? Math.max(
        1,
        Math.ceil(
          (new Date(selected.end_date).getTime() -
            new Date(selected.start_date).getTime()) /
            86400000,
        ),
      )
    : 0;
  const routeTotal = (selected?.stops.length ?? 0) * 1500;

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 rounded-full border-4 border-primary border-t-transparent animate-spin mx-auto mb-4" />
          <p className="text-on-surface-variant font-medium">Loading your graphs...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden bg-background" style={{ paddingTop: "64px" }}>
      {/* ── Left Sidebar ───────────────────────────────────────────────────── */}
      <aside className="w-[220px] flex-shrink-0 bg-surface-container-lowest border-r border-outline-variant/30 flex flex-col py-5 px-3 overflow-y-auto">
        <div className="px-2 mb-7">
          <p className="text-base font-black font-headline text-on-surface">TravelGraph</p>
          <p className="text-[10px] text-outline font-bold tracking-widest uppercase font-label mt-0.5">
            Kinetic Explorer
          </p>
        </div>

        <nav className="flex flex-col gap-0.5 flex-1">
          {NAV_ITEMS.map(({ key, icon, label, to }) => (
            <button
              key={key}
              onClick={() => {
                setActiveNav(key);
                if (to) navigate(to);
              }}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors text-left w-full ${
                activeNav === key
                  ? "bg-primary/10 text-primary font-bold"
                  : "text-on-surface-variant hover:bg-surface-container"
              }`}
            >
              <span className="material-symbols-outlined text-[18px]">{icon}</span>
              {label}
            </button>
          ))}
        </nav>

        <div className="mt-4 pt-4 border-t border-outline-variant/20">
          {user && (
            <div className="flex items-center gap-2 px-2 mb-4">
              <div className="w-8 h-8 rounded-full bg-primary text-on-primary flex items-center justify-center text-xs font-black flex-shrink-0">
                {user.name.charAt(0).toUpperCase()}
              </div>
              <div className="min-w-0">
                <p className="text-xs font-bold text-on-surface truncate">{user.name}</p>
                <p className="text-[10px] text-outline font-label">Explorer</p>
              </div>
            </div>
          )}
          <button
            onClick={() => setShowCreateForm(true)}
            className="w-full px-3 py-2.5 bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold text-xs rounded-xl hover:opacity-90 transition-all"
          >
            + Start Your Graph
          </button>
        </div>
      </aside>

      {/* ── Main Content ───────────────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col overflow-hidden min-w-0">
        {/* Top bar */}
        <div className="h-13 border-b border-outline-variant/30 flex items-center px-4 gap-3 bg-surface-container-lowest/60 flex-shrink-0 py-2">
          <div className="flex-1 max-w-xs relative">
            <span className="material-symbols-outlined absolute left-2.5 top-1/2 -translate-y-1/2 text-outline text-[16px]">
              search
            </span>
            <input
              type="text"
              placeholder="Search destinations..."
              className="w-full pl-8 pr-3 py-1.5 rounded-lg bg-surface-container text-on-surface text-sm border border-outline-variant/30 focus:outline-none focus:border-primary transition-colors"
            />
          </div>
          <div className="flex gap-1">
            {(["Explore", "Plan"] as const).map((tab) => (
              <button
                key={tab}
                className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-colors ${
                  tab === "Plan"
                    ? "bg-primary text-on-primary"
                    : "text-on-surface-variant hover:bg-surface-container"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
          <div className="ml-auto flex gap-1.5">
            <button className="w-8 h-8 rounded-lg bg-surface-container flex items-center justify-center text-on-surface-variant hover:bg-surface-container-high transition-colors">
              <span className="material-symbols-outlined text-[16px]">notifications</span>
            </button>
            <Link
              to="/profile"
              className="w-8 h-8 rounded-lg bg-primary text-on-primary flex items-center justify-center font-black text-xs"
            >
              {user?.name.charAt(0).toUpperCase() ?? "?"}
            </Link>
          </div>
        </div>

        {/* Itinerary selector strip */}
        <div className="flex items-center gap-2 px-4 py-2 border-b border-outline-variant/20 overflow-x-auto flex-shrink-0">
          {itineraries.map((it) => (
            <button
              key={it.id}
              onClick={() => setSelected(it)}
              className={`flex-shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-colors ${
                selected?.id === it.id
                  ? "bg-primary/10 text-primary border border-primary/30"
                  : "bg-surface-container text-on-surface-variant border border-outline-variant/20 hover:bg-surface-container-high"
              }`}
            >
              <span className="material-symbols-outlined text-[14px]">route</span>
              {it.title}
              <span
                role="button"
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeleteItinerary(it.id);
                }}
                className="text-error/50 hover:text-error ml-0.5 cursor-pointer leading-none"
              >
                ×
              </span>
            </button>
          ))}
          <button
            onClick={() => setShowCreateForm(true)}
            className="flex-shrink-0 flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold text-outline border border-outline-variant/30 hover:bg-surface-container transition-colors"
          >
            <span className="material-symbols-outlined text-[14px]">add</span>
            New
          </button>
        </div>

        {error && (
          <div className="mx-4 mt-2 bg-error-container text-on-error-container px-4 py-2 rounded-xl text-sm flex-shrink-0">
            {error}
          </div>
        )}

        <div className="flex-1 flex overflow-hidden min-h-0">
          {/* Graph Canvas */}
          <div className="flex-1 flex flex-col overflow-hidden min-w-0">
            <div
              className="flex-1 relative overflow-auto"
              style={{
                backgroundImage:
                  "radial-gradient(circle, rgba(148,163,184,0.35) 1px, transparent 1px)",
                backgroundSize: "28px 28px",
              }}
            >
              {!selected ? (
                <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-8">
                  <span className="material-symbols-outlined text-7xl text-outline/30 mb-4">
                    hub
                  </span>
                  <p className="text-on-surface-variant font-medium text-lg mb-2">
                    No graph selected
                  </p>
                  <p className="text-outline text-sm mb-6">
                    Create a new graph or select one from above
                  </p>
                  <button
                    onClick={() => setShowCreateForm(true)}
                    className="px-6 py-3 bg-primary text-on-primary font-bold rounded-xl text-sm hover:opacity-90 transition-all shadow-lg shadow-primary/20"
                  >
                    + Create Graph
                  </button>
                </div>
              ) : selected.stops.length === 0 ? (
                <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-8">
                  <span className="material-symbols-outlined text-6xl text-outline/30 mb-3">
                    add_location_alt
                  </span>
                  <p className="text-on-surface-variant font-medium mb-1">
                    No stops in "{selected.title}"
                  </p>
                  <p className="text-outline text-sm mb-5">
                    Add destinations to build your travel graph
                  </p>
                  <button
                    onClick={() => setShowStopForm(true)}
                    className="px-5 py-2.5 bg-primary text-on-primary font-bold rounded-xl text-sm hover:opacity-90 transition-all"
                  >
                    + Add First Stop
                  </button>
                </div>
              ) : (
                /* Graph nodes */
                <div
                  className="relative"
                  style={{ width: CANVAS_W, height: CANVAS_H, minWidth: "100%" }}
                >
                  {/* SVG edges */}
                  <svg
                    className="absolute inset-0 pointer-events-none"
                    width={CANVAS_W}
                    height={CANVAS_H}
                  >
                    {nodePositions.slice(0, -1).map((pos, i) => (
                      <line
                        key={i}
                        x1={pos.x + 30}
                        y1={pos.y + 30}
                        x2={nodePositions[i + 1].x + 30}
                        y2={nodePositions[i + 1].y + 30}
                        stroke="#003d9b"
                        strokeWidth="2"
                        strokeDasharray="7 5"
                        strokeOpacity="0.45"
                      />
                    ))}
                    {/* Close loop if >2 stops */}
                    {nodePositions.length > 2 && (
                      <line
                        x1={nodePositions[nodePositions.length - 1].x + 30}
                        y1={nodePositions[nodePositions.length - 1].y + 30}
                        x2={nodePositions[0].x + 30}
                        y2={nodePositions[0].y + 30}
                        stroke="#003d9b"
                        strokeWidth="1.5"
                        strokeDasharray="4 6"
                        strokeOpacity="0.2"
                      />
                    )}
                  </svg>

                  {/* Nodes */}
                  {selected.stops.map((stop, i) => {
                    const pos = nodePositions[i] ?? { x: 60 + i * 90, y: 60 };
                    return (
                      <div
                        key={stop.id}
                        className="absolute group"
                        style={{ left: pos.x, top: pos.y }}
                      >
                        <div className="w-[60px] h-[60px] rounded-full bg-primary text-on-primary flex flex-col items-center justify-center shadow-lg border-2 border-white/60 cursor-pointer hover:scale-110 transition-transform">
                          <span className="material-symbols-outlined text-[14px]">
                            location_on
                          </span>
                          <span className="text-[9px] font-bold text-center px-1 leading-tight">
                            {stop.destination_name.length > 7
                              ? stop.destination_name.slice(0, 7) + "…"
                              : stop.destination_name}
                          </span>
                        </div>
                        <div className="absolute -bottom-5 left-1/2 -translate-x-1/2 text-[10px] text-on-surface-variant font-bold whitespace-nowrap font-label">
                          Day {stop.day_number}
                        </div>
                        <button
                          onClick={() => handleDeleteStop(stop.id)}
                          className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-error text-white flex items-center justify-center text-[10px] font-bold opacity-0 group-hover:opacity-100 transition-opacity shadow"
                        >
                          ×
                        </button>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Bottom bar */}
            <div className="border-t border-outline-variant/30 flex items-center px-4 py-2.5 gap-6 bg-surface-container-lowest/60 flex-shrink-0">
              <div className="flex items-center gap-6 flex-1">
                <div>
                  <p className="text-[10px] font-bold text-outline uppercase tracking-widest font-label">
                    Route Total
                  </p>
                  <p className="text-sm font-black text-on-surface">
                    ₺{routeTotal.toLocaleString()}
                  </p>
                </div>
                <div>
                  <p className="text-[10px] font-bold text-outline uppercase tracking-widest font-label">
                    Stops
                  </p>
                  <p className="text-sm font-black text-on-surface">
                    {selected?.stops.length ?? 0}
                  </p>
                </div>
                <div>
                  <p className="text-[10px] font-bold text-outline uppercase tracking-widest font-label">
                    Travel Time
                  </p>
                  <p className="text-sm font-black text-on-surface">
                    {tripDays > 0 ? `${tripDays} Days` : "—"}
                  </p>
                </div>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setShowStopForm(true)}
                  disabled={!selected}
                  className="px-4 py-2 bg-surface-container text-on-surface border border-outline-variant/30 font-bold rounded-lg text-xs hover:bg-surface-container-high transition-colors disabled:opacity-40"
                >
                  + Add Stop
                </button>
                {selected && (
                  <Link
                    to={`/planner/${selected.id}/budget`}
                    className="px-5 py-2 bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold rounded-lg text-xs hover:opacity-90 transition-all"
                  >
                    Generate Itinerary →
                  </Link>
                )}
              </div>
            </div>
          </div>

          {/* ── Right Panel: FalkorDB Insights ─────────────────────────── */}
          <aside className="w-[270px] flex-shrink-0 border-l border-outline-variant/30 bg-surface-container-lowest/40 flex flex-col overflow-y-auto">
            <div className="px-4 py-3 border-b border-outline-variant/20 flex-shrink-0">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-primary text-[16px]">
                  hub
                </span>
                <p className="text-[11px] font-black text-on-surface uppercase tracking-widest font-label">
                  FalkorDB Insights
                </p>
              </div>
            </div>

            <div className="p-4 flex flex-col gap-4">
              {/* Best Next Stop */}
              <div className="bg-surface-container rounded-2xl p-4 border border-outline-variant/20">
                <p className="text-[10px] font-bold text-primary uppercase tracking-widest mb-3 font-label">
                  Best Next Stop
                </p>
                {suggestedDest ? (
                  <>
                    {suggestedDest.image_url && (
                      <img
                        src={suggestedDest.image_url}
                        alt={suggestedDest.name}
                        className="w-full h-24 object-cover rounded-xl mb-3"
                      />
                    )}
                    <p className="font-black text-on-surface text-sm mb-1">
                      {suggestedDest.name}
                    </p>
                    <p className="text-xs text-on-surface-variant mb-3">
                      Highly visited by graph travelers
                    </p>
                    <button
                      onClick={() => {
                        if (!selected) {
                          setShowCreateForm(true);
                        } else {
                          setSelectedDestId(suggestedDest.id);
                          setDayNumber((selected.stops.length ?? 0) + 1);
                          handleAddStop(suggestedDest.id);
                        }
                      }}
                      disabled={!selected}
                      className="w-full px-3 py-2 bg-primary text-on-primary font-bold rounded-lg text-xs hover:opacity-90 transition-all disabled:opacity-40"
                    >
                      + ADD TO GRAPH
                    </button>
                  </>
                ) : (
                  <p className="text-xs text-on-surface-variant">
                    All destinations added!
                  </p>
                )}
              </div>

              {/* Lunch Recommendation */}
              <div className="bg-surface-container rounded-2xl p-4 border border-outline-variant/20">
                <p className="text-[10px] font-bold text-primary uppercase tracking-widest mb-3 font-label">
                  Lunch Recommendation
                </p>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-secondary/10 flex items-center justify-center flex-shrink-0">
                    <span className="material-symbols-outlined text-secondary text-[18px]">
                      restaurant
                    </span>
                  </div>
                  <div>
                    <p className="text-xs font-bold text-on-surface">
                      {selected?.stops[0]?.destination_name
                        ? `Best in ${selected.stops[0].destination_name}`
                        : "Pick a stop first"}
                    </p>
                    <p className="text-[10px] text-on-surface-variant">
                      Local cuisine · Highly rated
                    </p>
                  </div>
                </div>
              </div>

              {/* Graph stats */}
              {selected && (
                <div className="bg-primary/5 rounded-2xl p-4 border border-primary/20">
                  <p className="text-[10px] font-bold text-primary uppercase tracking-widest mb-3 font-label">
                    Graph Analysis
                  </p>
                  <div className="flex flex-col gap-2.5">
                    {[
                      ["Nodes", selected.stops.length],
                      ["Edges", Math.max(0, selected.stops.length - 1)],
                      ["Countries", 1],
                      ["Est. Budget", `₺${routeTotal.toLocaleString()}`],
                    ].map(([label, val]) => (
                      <div key={String(label)} className="flex justify-between text-xs">
                        <span className="text-on-surface-variant">{label}</span>
                        <span className="font-bold text-on-surface">{val}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* FalkorDB badge */}
              <div className="flex items-center gap-2 px-3 py-2 bg-primary/5 rounded-xl border border-primary/15">
                <span className="material-symbols-outlined text-primary text-[14px]">
                  account_tree
                </span>
                <p className="text-[10px] font-bold text-primary font-label">
                  Powered by FalkorDB Graph
                </p>
              </div>
            </div>
          </aside>
        </div>
      </div>

      {/* ── Create itinerary modal ──────────────────────────────────────────── */}
      {showCreateForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm px-4">
          <div className="bg-surface-container-lowest rounded-3xl p-8 border border-outline-variant/30 shadow-2xl w-full max-w-md">
            <h2 className="text-xl font-black font-headline text-on-surface mb-6">
              New Travel Graph
            </h2>
            <div className="flex flex-col gap-4 mb-6">
              <div>
                <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                  Title
                </label>
                <input
                  className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Turkey Summer 2026"
                  autoFocus
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                    Start Date
                  </label>
                  <input
                    type="date"
                    className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                    End Date
                  </label>
                  <input
                    type="date"
                    className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                  />
                </div>
              </div>
            </div>
            {error && (
              <p className="text-error text-xs mb-4">{error}</p>
            )}
            <div className="flex gap-3">
              <button
                onClick={handleCreate}
                className="flex-1 py-3 bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold rounded-xl text-sm hover:opacity-90 transition-all"
              >
                Create Graph
              </button>
              <button
                onClick={() => {
                  setShowCreateForm(false);
                  setError("");
                }}
                className="px-6 py-3 bg-surface-container text-on-surface-variant font-bold rounded-xl text-sm hover:bg-surface-container-high transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ── Add stop modal ─────────────────────────────────────────────────── */}
      {showStopForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm px-4">
          <div className="bg-surface-container-lowest rounded-3xl p-8 border border-outline-variant/30 shadow-2xl w-full max-w-md">
            <h2 className="text-xl font-black font-headline text-on-surface mb-6">
              Add a Stop
            </h2>
            <div className="flex flex-col gap-4 mb-6">
              <div>
                <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                  Destination
                </label>
                <select
                  className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors"
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
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                    Day Number
                  </label>
                  <input
                    type="number"
                    min={1}
                    className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors"
                    value={dayNumber}
                    onChange={(e) => setDayNumber(Number(e.target.value))}
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                    Notes
                  </label>
                  <input
                    className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors"
                    value={stopNotes}
                    onChange={(e) => setStopNotes(e.target.value)}
                    placeholder="Optional notes"
                  />
                </div>
              </div>
            </div>
            {error && <p className="text-error text-xs mb-4">{error}</p>}
            <div className="flex gap-3">
              <button
                onClick={() => handleAddStop()}
                className="flex-1 py-3 bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold rounded-xl text-sm hover:opacity-90 transition-all"
              >
                Add to Graph
              </button>
              <button
                onClick={() => {
                  setShowStopForm(false);
                  setError("");
                }}
                className="px-6 py-3 bg-surface-container text-on-surface-variant font-bold rounded-xl text-sm hover:bg-surface-container-high transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default PlannerPage;
