import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { getItineraries } from "../api/itineraries";

const CITY_IMAGES: Record<string, string> = {
  Istanbul: "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=800",
  Cappadocia: "https://images.unsplash.com/photo-1570939274717-7eda259b50ed?w=800",
  Antalya: "https://images.unsplash.com/photo-1542051841857-5f90071e7989?w=800",
  Ephesus: "https://images.unsplash.com/photo-1589308078059-be1415eab4c3?w=800",
  Pamukkale: "https://images.unsplash.com/photo-1574351406668-5d2b6c040d94?w=800",
  Ankara: "https://images.unsplash.com/photo-1596423230819-3e77f2072a8a?w=800",
  Trabzon: "https://images.unsplash.com/photo-1634128221889-82ed6efebfc3?w=800",
  Bodrum: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
  Gaziantep: "https://images.unsplash.com/photo-1539814858141-928517f6afd3?w=800",
  Konya: "https://images.unsplash.com/photo-1636832557069-4e2ab74b3b3e?w=800",
};

function getCardImage(title: string): string {
  for (const [city, url] of Object.entries(CITY_IMAGES)) {
    if (title.toLowerCase().includes(city.toLowerCase())) return url;
  }
  return CITY_IMAGES["Istanbul"];
}

type Itinerary = {
  id: string;
  title: string;
  start_date: string;
  end_date: string;
  stops?: { id: string }[];
};

function ProfilePage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [itineraries, setItineraries] = useState<Itinerary[]>([]);
  const [loading, setLoading] = useState(true);
  const [currency, setCurrency] = useState<"TRY" | "EUR" | "USD">("TRY");
  const [aiLevel, setAiLevel] = useState(75);

  useEffect(() => {
    if (!user) {
      navigate("/login");
      return;
    }
    getItineraries()
      .then((data) => setItineraries(data ?? []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [user]);

  if (!user) return null;

  const initials = user.name
    .split(" ")
    .map((n) => n.charAt(0))
    .join("")
    .toUpperCase()
    .slice(0, 2);

  return (
    <div className="bg-background min-h-screen pt-24 pb-16 px-6">
      <div className="max-w-screen-xl mx-auto">

        {/* ── User Hero ───────────────────────────────────────────────────── */}
        <div className="flex items-start gap-6 mb-12 flex-wrap">
          {/* Avatar */}
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary to-primary-container text-on-primary flex items-center justify-center text-3xl font-black font-headline shadow-lg flex-shrink-0">
            {initials}
          </div>

          <div className="flex-1 min-w-0">
            <div className="flex items-center flex-wrap gap-3 mb-1">
              <h1 className="text-3xl font-black font-headline text-on-surface tracking-tight">
                {user.name}
              </h1>
              <span className="px-3 py-1 bg-primary text-on-primary text-[10px] font-bold tracking-widest rounded-full uppercase font-label">
                PRO EXPLORER
              </span>
            </div>
            <p className="text-on-surface-variant text-sm mb-5">
              Kinetic Architect &amp; Global Nomad
            </p>
            <div className="flex gap-8 flex-wrap">
              {[
                { label: "Graphs Created", value: itineraries.length },
                { label: "Countries", value: 1 },
                { label: "KM Traveled", value: "—" },
              ].map(({ label, value }) => (
                <div key={label}>
                  <p className="text-2xl font-black font-headline text-on-surface">
                    {value}
                  </p>
                  <p className="text-xs text-outline uppercase tracking-widest font-label">
                    {label}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <button
            onClick={() => {
              logout();
              navigate("/");
            }}
            className="px-4 py-2 border border-outline-variant/40 text-on-surface-variant rounded-xl text-sm font-bold hover:bg-surface-container transition-colors flex-shrink-0"
          >
            Sign Out
          </button>
        </div>

        {/* ── Saved Graphs ────────────────────────────────────────────────── */}
        <section className="mb-14">
          <div className="flex items-center gap-4 mb-6">
            <span className="text-[10px] font-bold text-outline uppercase tracking-widest font-label">
              Portfolio
            </span>
            <div className="flex-1 h-px bg-outline-variant/30" />
          </div>
          <div className="flex items-end justify-between mb-6 gap-4">
            <h2 className="text-2xl font-black font-headline text-on-surface">
              Saved Graphs
            </h2>
            <Link
              to="/planner"
              className="text-sm font-bold text-primary hover:underline"
            >
              + New Graph
            </Link>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div
                  key={i}
                  className="h-60 bg-surface-container-low rounded-3xl animate-pulse"
                />
              ))}
            </div>
          ) : itineraries.length === 0 ? (
            <div className="bg-surface-container-lowest rounded-3xl p-14 text-center border border-outline-variant/30 shadow-card">
              <span className="material-symbols-outlined text-5xl text-outline/40 mb-3 block">
                map
              </span>
              <p className="text-on-surface-variant font-medium mb-5">
                No travel graphs yet.
              </p>
              <Link
                to="/planner"
                className="inline-block px-6 py-3 bg-primary text-on-primary font-bold rounded-xl text-sm hover:opacity-90 transition-all"
              >
                Open Planner
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {itineraries.map((it) => {
                const days = Math.max(
                  1,
                  Math.ceil(
                    (new Date(it.end_date).getTime() -
                      new Date(it.start_date).getTime()) /
                      86400000,
                  ),
                );
                const stops = it.stops?.length ?? 0;
                const budget = stops * 1500;
                const img = getCardImage(it.title);
                return (
                  <div
                    key={it.id}
                    className="bg-surface-container-lowest rounded-3xl overflow-hidden border border-outline-variant/30 shadow-card hover:shadow-2xl transition-all hover:-translate-y-1"
                  >
                    <div className="h-40 relative overflow-hidden">
                      <img
                        src={img}
                        alt={it.title}
                        className="w-full h-full object-cover"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
                      <span className="absolute top-3 right-3 px-2 py-1 bg-black/40 backdrop-blur text-white text-[10px] font-bold rounded-lg border border-white/20 font-label">
                        {stops} stops
                      </span>
                    </div>
                    <div className="p-5">
                      <h3 className="font-black font-headline text-on-surface mb-3 tracking-tight">
                        {it.title}
                      </h3>
                      <div className="flex justify-between text-xs text-on-surface-variant mb-1 font-label">
                        <span>ESTIMATED BUDGET</span>
                        <span className="font-bold text-on-surface">
                          ₺{budget.toLocaleString()}
                        </span>
                      </div>
                      <div className="flex justify-between text-xs text-on-surface-variant mb-5 font-label">
                        <span>DURATION</span>
                        <span className="font-bold text-on-surface">{days} Days</span>
                      </div>
                      <Link
                        to="/planner"
                        className="block text-center px-4 py-2.5 bg-primary/10 text-primary font-bold rounded-xl text-xs hover:bg-primary/20 transition-colors"
                      >
                        Open in Planner
                      </Link>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </section>

        {/* ── Preferences ─────────────────────────────────────────────────── */}
        <section>
          <div className="flex items-center gap-4 mb-6">
            <span className="text-[10px] font-bold text-outline uppercase tracking-widest font-label">
              Settings
            </span>
            <div className="flex-1 h-px bg-outline-variant/30" />
          </div>
          <h2 className="text-2xl font-black font-headline text-on-surface mb-6">
            Preferences
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Currency */}
            <div className="bg-surface-container-lowest rounded-3xl p-6 border border-outline-variant/30 shadow-card">
              <p className="text-xs font-bold text-outline uppercase tracking-widest mb-4 font-label">
                Currency
              </p>
              <div className="flex gap-2 mb-4">
                {(
                  [
                    ["TRY", "₺ TRY"],
                    ["EUR", "€ EUR"],
                    ["USD", "$ USD"],
                  ] as const
                ).map(([c, label]) => (
                  <button
                    key={c}
                    onClick={() => setCurrency(c)}
                    className={`px-4 py-2 rounded-lg font-bold text-sm transition-colors ${
                      currency === c
                        ? "bg-primary text-on-primary shadow-card"
                        : "bg-surface-container text-on-surface-variant hover:bg-surface-container-high"
                    }`}
                  >
                    {label}
                  </button>
                ))}
              </div>
              <div className="flex items-center gap-2 text-xs text-on-surface-variant">
                <span className="material-symbols-outlined text-[14px] text-outline">
                  straighten
                </span>
                Measurement: Metric (km) — active
              </div>
            </div>

            {/* AI Insight Level */}
            <div className="bg-surface-container-lowest rounded-3xl p-6 border border-outline-variant/30 shadow-card">
              <div className="flex items-center justify-between mb-4">
                <p className="text-xs font-bold text-outline uppercase tracking-widest font-label">
                  AI Insight Level
                </p>
                <span className="flex items-center gap-1 px-2 py-1 bg-primary/10 text-primary text-[10px] font-bold rounded-full font-label">
                  <span className="material-symbols-outlined text-[12px]">hub</span>
                  FalkorDB Powered
                </span>
              </div>
              <input
                type="range"
                min={0}
                max={100}
                value={aiLevel}
                onChange={(e) => setAiLevel(Number(e.target.value))}
                className="w-full accent-primary mb-2"
              />
              <div className="flex justify-between text-xs text-on-surface-variant">
                <span>Basic</span>
                <span className="font-black text-primary">{aiLevel}%</span>
                <span>Maximum</span>
              </div>
              <p className="text-xs text-outline mt-3">
                Higher levels use deeper graph traversal for recommendations.
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default ProfilePage;
