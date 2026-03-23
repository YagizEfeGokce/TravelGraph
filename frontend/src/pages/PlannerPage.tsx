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
      <div className="min-h-screen bg-background flex items-center justify-center pt-24">
        <div className="text-center">
          <div className="w-12 h-12 rounded-full border-4 border-primary border-t-transparent animate-spin mx-auto mb-4" />
          <p className="text-on-surface-variant font-medium">Loading your plans...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-background min-h-screen pt-24 pb-16 px-6">
      <div className="max-w-screen-xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-start mb-10 gap-4 flex-wrap">
          <div>
            <span className="inline-block px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed text-[10px] font-bold tracking-widest uppercase mb-3 font-label">
              Route Planner
            </span>
            <h1 className="text-5xl font-black font-headline text-on-surface tracking-tight">
              Trip Planner
            </h1>
            <p className="text-on-surface-variant mt-2">
              Create and manage your travel itineraries.
            </p>
          </div>
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="px-6 py-3 bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold rounded-xl shadow-card hover:opacity-90 transition-all mt-4 md:mt-0"
          >
            + New Plan
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-error-container text-on-error-container px-4 py-3 rounded-xl text-sm mb-6">
            {error}
          </div>
        )}

        {/* Create form */}
        {showCreateForm && (
          <div className="bg-surface-container-lowest rounded-3xl p-6 border border-outline-variant/30 shadow-card mb-8">
            <h2 className="text-xl font-black font-headline text-on-surface mb-5">
              New Itinerary
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-5">
              <div>
                <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                  Title
                </label>
                <input
                  className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Turkey Summer 2025"
                />
              </div>
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
            <div className="flex gap-3">
              <button
                onClick={handleCreate}
                className="px-6 py-2.5 bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold rounded-xl text-sm hover:opacity-90 transition-all"
              >
                Create
              </button>
              <button
                onClick={() => setShowCreateForm(false)}
                className="px-6 py-2.5 bg-surface-container text-on-surface-variant font-bold rounded-xl text-sm hover:bg-surface-container-high transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* Two-column layout */}
        <div className="grid grid-cols-1 md:grid-cols-[280px_1fr] gap-6">
          {/* Plans list */}
          <div>
            <p className="text-xs font-bold text-outline uppercase tracking-widest mb-4 font-label">
              My Plans
            </p>
            {itineraries.length === 0 ? (
              <div className="bg-surface-container-lowest rounded-2xl p-8 text-center border border-outline-variant/30 shadow-card">
                <p className="text-on-surface-variant text-sm">
                  No plans yet.
                  <br />
                  Create one to get started!
                </p>
              </div>
            ) : (
              <div className="flex flex-col gap-3">
                {itineraries.map((it) => (
                  <div
                    key={it.id}
                    onClick={() => setSelected(it)}
                    className={`bg-surface-container-lowest rounded-2xl p-4 border-2 cursor-pointer transition-all shadow-card hover:shadow-ambient ${
                      selected?.id === it.id
                        ? "border-primary"
                        : "border-outline-variant/30 hover:border-primary/30"
                    }`}
                  >
                    <div className="font-bold text-on-surface text-sm mb-1">{it.title}</div>
                    <div className="text-xs text-on-surface-variant mb-1">
                      {it.start_date} → {it.end_date}
                    </div>
                    <div className="text-xs text-outline mb-3">
                      {it.stops?.length ?? 0} stop{it.stops?.length !== 1 ? "s" : ""}
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeleteItinerary(it.id);
                      }}
                      className="px-3 py-1 text-xs font-bold text-error bg-error-container/50 rounded-lg hover:bg-error-container transition-colors"
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
              <div className="bg-surface-container-lowest rounded-3xl p-16 text-center border border-outline-variant/30 shadow-card">
                <span className="material-symbols-outlined text-5xl text-outline mb-4 block">
                  map
                </span>
                <p className="text-on-surface-variant">
                  Select a plan from the left to manage its stops.
                </p>
              </div>
            ) : (
              <>
                {/* Plan header */}
                <div className="bg-surface-container-lowest rounded-3xl p-6 border border-outline-variant/30 shadow-card mb-5">
                  <div className="flex justify-between items-start mb-5 gap-4">
                    <div>
                      <h2 className="text-2xl font-black font-headline text-on-surface tracking-tight">
                        {selected.title}
                      </h2>
                      <p className="text-sm text-on-surface-variant mt-1">
                        {selected.start_date} → {selected.end_date}
                      </p>
                    </div>
                    <Link
                      to={`/planner/${selected.id}/budget`}
                      className="px-4 py-2 bg-gradient-to-br from-secondary to-on-secondary-container text-on-secondary font-bold rounded-xl text-sm shadow-card hover:opacity-90 transition-all"
                    >
                      Budget Planner
                    </Link>
                  </div>

                  {/* Stops */}
                  {selected.stops.length === 0 ? (
                    <p className="text-on-surface-variant text-sm">
                      No stops yet. Add your first destination!
                    </p>
                  ) : (
                    <div className="flex flex-col gap-3">
                      {selected.stops.map((stop) => (
                        <div
                          key={stop.id}
                          className="flex justify-between items-center px-4 py-3 rounded-xl bg-surface-container border border-outline-variant/20"
                        >
                          <div>
                            <span className="font-bold text-primary text-xs mr-2 font-label uppercase tracking-widest">
                              Day {stop.day_number}
                            </span>
                            <span className="font-bold text-on-surface text-sm">
                              {stop.destination_name}
                            </span>
                            {stop.notes && (
                              <p className="text-xs text-on-surface-variant mt-1">{stop.notes}</p>
                            )}
                          </div>
                          <button
                            onClick={() => handleDeleteStop(stop.id)}
                            className="w-7 h-7 flex items-center justify-center rounded-lg bg-error-container/50 text-error hover:bg-error-container transition-colors text-xs font-bold"
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
                  <div className="bg-surface-container-lowest rounded-3xl p-6 border border-outline-variant/30 shadow-card">
                    <h3 className="font-black font-headline text-on-surface mb-5">
                      Add a Stop
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
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
                    </div>
                    <div className="mb-4">
                      <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                        Notes (optional)
                      </label>
                      <input
                        className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors"
                        value={stopNotes}
                        onChange={(e) => setStopNotes(e.target.value)}
                        placeholder="e.g. Arrive by train, check in early"
                      />
                    </div>
                    <div className="flex gap-3">
                      <button
                        onClick={handleAddStop}
                        className="px-6 py-2.5 bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold rounded-xl text-sm hover:opacity-90 transition-all"
                      >
                        Add Stop
                      </button>
                      <button
                        onClick={() => setShowStopForm(false)}
                        className="px-6 py-2.5 bg-surface-container text-on-surface-variant font-bold rounded-xl text-sm hover:bg-surface-container-high transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <button
                    onClick={() => setShowStopForm(true)}
                    className="px-6 py-3 bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold rounded-xl shadow-card hover:opacity-90 transition-all"
                  >
                    + Add Stop
                  </button>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PlannerPage;
