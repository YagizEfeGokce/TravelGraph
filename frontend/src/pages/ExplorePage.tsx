import { useMemo, useState } from "react";
import { useDestinations } from "../hooks/useDestinations";
import DestinationCard from "../components/DestinationCard";

function ExplorePage() {
  const { destinations, loading } = useDestinations();

  const [category, setCategory] = useState("All");
  const [season, setSeason] = useState("All");
  const [city, setCity] = useState("All");

  const categories = ["All", "Culture", "History", "Beach", "Nature", "Food", "City"];
  const seasons = ["All", "Spring", "Summer", "Autumn", "Winter"];

  const cities = useMemo(() => {
    const unique = Array.from(new Set(destinations.map((d) => d.city).filter(Boolean))).sort();
    return unique as string[];
  }, [destinations]);

  const filtered = useMemo(() => {
    return destinations.filter((dest) => {
      const catOk = category === "All" || dest.category === category;
      const seaOk = season === "All" || dest.season === season;
      const citOk = city === "All" || dest.city === city;
      return catOk && seaOk && citOk;
    });
  }, [destinations, category, season, city]);

  return (
    <div className="bg-background min-h-screen pt-24 pb-16 px-6">
      <div className="max-w-screen-2xl mx-auto">
        {/* Header */}
        <div className="mb-10">
          <span className="inline-block px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed text-[10px] font-bold tracking-widest uppercase mb-3 font-label">
            Destination Discovery
          </span>
          <h1 className="text-5xl md:text-6xl font-black font-headline text-on-surface tracking-tight mb-4">
            Explore Destinations
          </h1>
          <p className="text-on-surface-variant max-w-2xl leading-relaxed text-lg">
            Filter destinations across Turkey by travel category, best season
            and city to discover the places that fit your travel style.
          </p>
        </div>

        {/* Filters */}
        <div className="bg-surface-container-lowest rounded-3xl p-6 border border-outline-variant/30 shadow-card mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                Category
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 font-medium text-sm focus:outline-none focus:border-primary transition-colors"
              >
                {categories.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                Season
              </label>
              <select
                value={season}
                onChange={(e) => setSeason(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 font-medium text-sm focus:outline-none focus:border-primary transition-colors"
              >
                {seasons.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                City
              </label>
              <select
                value={city}
                onChange={(e) => setCity(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 font-medium text-sm focus:outline-none focus:border-primary transition-colors"
              >
                <option key="__all" value="All">All</option>
                {cities.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Result count */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
          <div className="flex items-center gap-3 flex-wrap">
            <span className="px-4 py-2 rounded-full bg-primary/10 text-primary font-bold text-sm font-label">
              {loading ? "..." : filtered.length} destinations found
            </span>
            {(category !== "All" || season !== "All" || city !== "All") && (
              <button
                onClick={() => { setCategory("All"); setSeason("All"); setCity("All"); }}
                className="px-3 py-1.5 rounded-full border border-outline-variant text-on-surface-variant text-xs font-medium hover:bg-surface-container-low transition-colors"
              >
                Clear filters
              </button>
            )}
          </div>
          <p className="text-on-surface-variant text-sm">
            Filter results update instantly according to your selection.
          </p>
        </div>

        {/* Grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
              <div key={i} className="h-56 rounded-3xl bg-surface-container-low animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filtered.map((dest) => (
              <DestinationCard
                key={dest.id}
                id={dest.id}
                name={dest.name}
                country={dest.country}
                description={dest.description}
                category={dest.category}
                season={dest.season}
              />
            ))}
          </div>
        )}

        {!loading && filtered.length === 0 && (
          <div className="text-center py-20 text-on-surface-variant">
            <p className="text-lg font-medium">No destinations match your filters.</p>
            <p className="text-sm mt-2">Try adjusting the category, season or city.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ExplorePage;
