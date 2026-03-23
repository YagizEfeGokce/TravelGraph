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

function getCityImage(city: string): string {
  return CITY_IMAGES[city] ?? CITY_IMAGES["Istanbul"];
}

type FestType = "All Events" | "Music" | "Art" | "Food & Drink" | "Culture" | "Sports";

function getFestivalType(name: string): FestType {
  const l = name.toLowerCase();
  if (l.includes("jazz") || l.includes("music") || l.includes("akcaabat") || l.includes("akçaabat")) return "Music";
  if (l.includes("film") || l.includes("ballet") || l.includes("culture") || l.includes("tulip")) return "Art";
  if (l.includes("gastronomy") || l.includes("baklava") || l.includes("food")) return "Food & Drink";
  if (l.includes("triathlon") || l.includes("sport")) return "Sports";
  return "Culture";
}

function formatDate(dateStr: string): { month: string; day: string } {
  const d = new Date(dateStr + "T00:00:00");
  return {
    month: d.toLocaleString("en", { month: "short" }).toUpperCase(),
    day: String(d.getDate()).padStart(2, "0"),
  };
}

const TYPE_FILTERS: FestType[] = ["All Events", "Music", "Art", "Food & Drink", "Culture", "Sports"];

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
  const [typeFilter, setTypeFilter] = useState<FestType>("All Events");
  const [timeFilter, setTimeFilter] = useState<"all" | "upcoming" | "3months" | "year">("all");

  useEffect(() => {
    getFestivals()
      .then(setFestivals)
      .catch(() => setError("Could not load festivals."))
      .finally(() => setLoading(false));
  }, []);

  const cities = useMemo(
    () => Array.from(new Set(festivals.map((f) => f.city).filter(Boolean))).sort(),
    [festivals],
  );

  // Next upcoming festival
  const nextFestival = useMemo(() => {
    const upcoming = festivals
      .filter((f) => f.start_date >= TODAY)
      .sort((a, b) => a.start_date.localeCompare(b.start_date));
    return upcoming[0] ?? null;
  }, [festivals]);

  const filtered = useMemo(() => {
    let list = festivals;
    if (selectedCity !== "All") list = list.filter((f) => f.city === selectedCity);
    if (typeFilter !== "All Events") list = list.filter((f) => getFestivalType(f.name) === typeFilter);
    if (searchText.trim()) {
      const q = searchText.toLowerCase();
      list = list.filter(
        (f) =>
          f.name.toLowerCase().includes(q) ||
          f.city.toLowerCase().includes(q) ||
          f.description.toLowerCase().includes(q),
      );
    }
    if (timeFilter === "upcoming") list = list.filter((f) => f.end_date >= TODAY);
    else if (timeFilter === "3months") {
      const cut = addMonths(3);
      list = list.filter((f) => f.start_date >= TODAY && f.start_date <= cut);
    } else if (timeFilter === "year") {
      const cut = addMonths(12);
      list = list.filter((f) => f.start_date >= TODAY && f.start_date <= cut);
    }
    return list;
  }, [festivals, selectedCity, typeFilter, searchText, timeFilter]);

  return (
    <div className="bg-background min-h-screen pt-24 pb-16 px-6">
      <div className="max-w-screen-2xl mx-auto">

        {/* ── Header ──────────────────────────────────────────────────────── */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10">
          <div>
            <span className="inline-block px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed text-[10px] font-bold tracking-widest uppercase mb-3 font-label">
              Event Explorer
            </span>
            <h1 className="text-5xl md:text-6xl font-black font-headline text-on-surface tracking-tight mb-3">
              Festival Calendar
            </h1>
            <p className="text-on-surface-variant max-w-xl leading-relaxed">
              Discover Turkey's festivals and cultural events — powered by graph intelligence.
            </p>
          </div>

          {/* Next Major Node card */}
          {nextFestival && (
            <div className="flex-shrink-0 bg-surface-container-lowest rounded-2xl p-4 border border-primary/30 shadow-card min-w-[220px]">
              <p className="text-[10px] font-bold text-primary uppercase tracking-widest mb-2 font-label">
                Next Major Node
              </p>
              <p className="font-black text-on-surface text-sm mb-0.5">{nextFestival.name}</p>
              <p className="text-xs text-on-surface-variant mb-2">{nextFestival.city} · Turkey</p>
              <div className="flex items-center gap-1.5 text-xs text-primary font-bold">
                <span className="material-symbols-outlined text-[14px]">calendar_month</span>
                {nextFestival.start_date}
              </div>
            </div>
          )}
        </div>

        {/* ── Filters ─────────────────────────────────────────────────────── */}
        <div className="bg-surface-container-lowest rounded-3xl p-5 border border-outline-variant/30 shadow-card mb-6">
          <div className="flex flex-wrap gap-3 items-center mb-4">
            {/* Search */}
            <div className="flex-1 min-w-[200px] relative">
              <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline text-[16px]">
                search
              </span>
              <input
                type="text"
                placeholder="Search events..."
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors placeholder:text-outline"
              />
            </div>

            {/* City select */}
            <select
              value={selectedCity}
              onChange={(e) => setSelectedCity(e.target.value)}
              className="px-4 py-2.5 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 font-medium text-sm focus:outline-none focus:border-primary transition-colors"
            >
              <option key="__all" value="All">All Cities</option>
              {cities.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>

            {/* Time filter */}
            <div className="flex gap-1.5 flex-wrap">
              {(
                [
                  ["all", "All"],
                  ["upcoming", "Upcoming"],
                  ["3months", "3 Months"],
                  ["year", "This Year"],
                ] as const
              ).map(([val, label]) => (
                <button
                  key={val}
                  onClick={() => setTimeFilter(val)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    timeFilter === val
                      ? "bg-primary text-on-primary shadow-card"
                      : "bg-surface-container text-on-surface-variant border border-outline-variant/30 hover:bg-surface-container-high"
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          {/* Type filter chips */}
          <div className="flex gap-2 flex-wrap">
            {TYPE_FILTERS.map((t) => (
              <button
                key={t}
                onClick={() => setTypeFilter(t)}
                className={`px-3 py-1.5 rounded-full text-xs font-bold transition-all ${
                  typeFilter === t
                    ? "bg-primary text-on-primary"
                    : "bg-surface-container-high text-on-surface-variant hover:bg-outline-variant/20"
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {/* Result count */}
        <p className="text-on-surface-variant text-sm mb-6 font-label">
          {loading
            ? "Loading..."
            : `${filtered.length} festival${filtered.length !== 1 ? "s" : ""} found`}
        </p>

        {error && (
          <div className="bg-error-container text-on-error-container px-4 py-3 rounded-xl text-sm mb-6">
            {error}
          </div>
        )}

        {/* ── Grid ────────────────────────────────────────────────────────── */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="h-72 rounded-3xl bg-surface-container-low animate-pulse" />
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-24 text-on-surface-variant">
            <span className="material-symbols-outlined text-5xl text-outline/30 block mb-3">
              event_busy
            </span>
            <p className="text-lg font-medium">No festivals match your filters.</p>
            <p className="text-sm mt-2">Try adjusting the search or filters.</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filtered.map((festival) => {
                const { month, day } = formatDate(festival.start_date);
                const festType = getFestivalType(festival.name);
                const isPast = festival.end_date < TODAY;
                return (
                  <div
                    key={festival.id}
                    className={`bg-surface-container-lowest rounded-3xl overflow-hidden border border-outline-variant/30 shadow-card hover:shadow-2xl transition-all hover:-translate-y-1 ${isPast ? "opacity-60" : ""}`}
                  >
                    {/* City image */}
                    <div className="relative h-44 overflow-hidden">
                      <img
                        src={getCityImage(festival.city)}
                        alt={festival.city}
                        className="w-full h-full object-cover"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/10 to-transparent" />

                      {/* Date badge */}
                      <div className="absolute top-3 left-3 bg-white rounded-xl overflow-hidden shadow-lg text-center w-12">
                        <div className="bg-primary py-1 px-2">
                          <p className="text-[9px] font-black text-on-primary tracking-widest">
                            {month}
                          </p>
                        </div>
                        <div className="py-1 px-2">
                          <p className="text-lg font-black text-on-surface leading-none">{day}</p>
                        </div>
                      </div>

                      {/* Type chip */}
                      <span className="absolute top-3 right-3 px-2.5 py-1 bg-black/40 backdrop-blur text-white text-[10px] font-bold rounded-lg border border-white/20 font-label">
                        {festType}
                      </span>

                      {/* City label */}
                      <div className="absolute bottom-3 left-4">
                        <p className="text-white font-bold text-sm">{festival.city}</p>
                        <p className="text-white/70 text-xs">Turkey</p>
                      </div>
                    </div>

                    <div className="p-5">
                      <h3 className="text-base font-black font-headline text-on-surface mb-2 tracking-tight leading-snug">
                        {festival.name}
                      </h3>
                      <p className="text-sm text-on-surface-variant leading-relaxed mb-4 line-clamp-2">
                        {festival.description}
                      </p>

                      <div className="flex items-center justify-between">
                        <div className="flex flex-col gap-1">
                          <div className="flex items-center gap-1.5 text-xs text-on-surface-variant">
                            <span className="material-symbols-outlined text-[13px] text-primary">
                              calendar_month
                            </span>
                            <span>
                              {festival.start_date}
                              {festival.end_date !== festival.start_date &&
                                ` – ${festival.end_date}`}
                            </span>
                          </div>
                          {festival.ticket_price != null && (
                            <span className="text-xs font-bold text-primary font-label">
                              {festival.ticket_price === 0
                                ? "🎟 Free entry"
                                : `🎟 ₺${festival.ticket_price}`}
                            </span>
                          )}
                        </div>
                        <button className="w-8 h-8 rounded-xl bg-primary/10 text-primary flex items-center justify-center hover:bg-primary/20 transition-colors" title="Add to route">
                          <span className="material-symbols-outlined text-[16px]">add</span>
                        </button>
                      </div>

                      {festival.is_recurring && (
                        <div className="mt-3 flex items-center gap-1 text-[10px] font-bold text-outline uppercase tracking-widest font-label">
                          <span className="material-symbols-outlined text-[12px]">autorenew</span>
                          Annual event
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Empty state footer card */}
            <div className="mt-10 bg-surface-container-low rounded-3xl p-10 text-center border border-outline-variant/20">
              <span className="material-symbols-outlined text-4xl text-outline/40 mb-3 block">
                explore
              </span>
              <p className="text-on-surface-variant font-medium">
                Find more events at your next destination
              </p>
              <p className="text-outline text-sm mt-1">
                Visit a destination page to see local festivals and cultural events.
              </p>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default FestivalsPage;
