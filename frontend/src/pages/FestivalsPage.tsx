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

  return (
    <div className="bg-background min-h-screen pt-24 pb-16 px-6">
      <div className="max-w-screen-2xl mx-auto">
        {/* Header */}
        <div className="mb-10">
          <span className="inline-block px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed text-[10px] font-bold tracking-widest uppercase mb-3 font-label">
            Events & Culture
          </span>
          <h1 className="text-5xl md:text-6xl font-black font-headline text-on-surface tracking-tight mb-4">
            Festival Calendar
          </h1>
          <p className="text-on-surface-variant max-w-2xl leading-relaxed text-lg">
            Discover festivals and cultural events across Turkey.
          </p>
        </div>

        {/* Filters */}
        <div className="bg-surface-container-lowest rounded-3xl p-6 border border-outline-variant/30 shadow-card mb-8">
          <div className="flex flex-wrap gap-4 items-center">
            <div className="flex-1 min-w-[220px]">
              <input
                type="text"
                placeholder="Search festivals or cities..."
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors placeholder:text-outline"
              />
            </div>

            <div className="min-w-[180px]">
              <select
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 font-medium text-sm focus:outline-none focus:border-primary transition-colors"
              >
                <option key="__all" value="All">All Cities</option>
                {cities.filter(Boolean).map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex gap-2 flex-wrap">
              {(
                [
                  ["all", "All"],
                  ["upcoming", "Upcoming"],
                  ["3months", "Next 3 Months"],
                  ["year", "This Year"],
                ] as const
              ).map(([val, label]) => (
                <button
                  key={val}
                  onClick={() => setTimeFilter(val)}
                  className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${
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

        {/* Grid */}
        {!loading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filtered.length === 0 ? (
              <div className="col-span-full text-center py-20 text-on-surface-variant">
                <p className="text-lg font-medium">No festivals match your filters.</p>
                <p className="text-sm mt-2">Try adjusting the search or time filter.</p>
              </div>
            ) : (
              filtered.map((festival) => (
                <div
                  key={festival.id}
                  className="bg-surface-container-lowest rounded-3xl overflow-hidden border border-outline-variant/30 shadow-card hover:shadow-2xl transition-shadow"
                >
                  {/* Color bar top */}
                  <div className="h-1.5 bg-gradient-to-r from-primary to-primary-container" />

                  <div className="p-6">
                    <div className="flex items-start justify-between gap-3 mb-3">
                      <span className="px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed text-[10px] font-bold tracking-widest uppercase font-label">
                        {festival.city}
                      </span>
                      {festival.ticket_price != null && (
                        <span className="text-sm font-bold text-primary font-label">
                          {festival.ticket_price === 0 ? "Free" : `₺${festival.ticket_price}`}
                        </span>
                      )}
                    </div>

                    <h3 className="text-lg font-black font-headline text-on-surface mb-2 tracking-tight">
                      {festival.name}
                    </h3>

                    <p className="text-sm text-on-surface-variant leading-relaxed mb-4">
                      {festival.description}
                    </p>

                    <div className="flex flex-col gap-1.5">
                      <div className="flex items-center gap-2 text-xs text-on-surface-variant font-label">
                        <span className="material-symbols-outlined text-sm text-primary">calendar_month</span>
                        <span>
                          {festival.start_date}
                          {festival.end_date !== festival.start_date && ` → ${festival.end_date}`}
                        </span>
                      </div>

                      {festival.is_recurring && (
                        <span className="inline-flex items-center gap-1 text-[10px] font-bold text-outline uppercase tracking-widest font-label mt-1">
                          <span className="material-symbols-outlined text-xs">autorenew</span>
                          Annual event
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {loading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="h-52 rounded-3xl bg-surface-container-low animate-pulse" />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default FestivalsPage;
