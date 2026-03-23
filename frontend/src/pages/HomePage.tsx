import { Link } from "react-router-dom";
import { useDestinations } from "../hooks/useDestinations";
import DestinationCard from "../components/DestinationCard";

function HomePage() {
  const { destinations, loading } = useDestinations();
  const featuredDestinations = destinations.slice(0, 6);

  return (
    <div className="bg-background min-h-screen">
      {/* Hero Section */}
      <section className="relative px-6 pt-32 pb-20 overflow-hidden">
        <div className="max-w-screen-2xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div className="lg:col-span-7 z-10">
            <span className="inline-block px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed text-[10px] font-bold tracking-widest uppercase mb-4 font-label">
              The Intelligent Cartographer
            </span>
            <h1 className="text-6xl md:text-8xl font-black font-headline text-on-surface leading-[0.9] tracking-tighter mb-6">
              Map Your <br />
              <span className="text-primary italic">Soul's Journey.</span>
            </h1>
            <p className="text-xl text-on-surface-variant max-w-xl mb-10 leading-relaxed">
              Transcend standard itineraries. TravelGraph turns complex logistics into a fluid network
              of discovery, connecting you to the world's most intentional paths.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link
                to="/explore"
                className="px-8 py-4 bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold rounded-lg shadow-xl shadow-primary/20 hover:scale-105 transition-transform"
              >
                Start Exploring
              </Link>
              <Link
                to="/planner"
                className="px-8 py-4 border border-outline-variant text-primary font-bold rounded-lg hover:bg-surface-container-low transition-colors"
              >
                View Planner
              </Link>
            </div>
          </div>

          <div className="lg:col-span-5 relative">
            <div className="relative rounded-[2rem] overflow-hidden aspect-[4/5] shadow-2xl bg-surface-container-high">
              <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-secondary/20" />
              <div className="absolute inset-0 node-edge-motif" />
              <div className="absolute bottom-8 left-8 right-8 p-6 glass-nav rounded-2xl border border-white/20">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold text-primary tracking-widest uppercase mb-1 font-label">
                      Current Hotspot
                    </p>
                    <h3 className="text-2xl font-bold font-headline text-on-surface">
                      {loading ? "Loading..." : destinations[0]?.name || "Discover the World"}
                    </h3>
                  </div>
                  <div className="w-12 h-12 rounded-full bg-primary-container flex items-center justify-center text-on-primary">
                    <span className="material-symbols-outlined">north_east</span>
                  </div>
                </div>
              </div>
            </div>
            <div className="absolute -top-6 -right-6 w-32 h-32 node-edge-motif rounded-full" />
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="px-6 mb-24">
        <div className="max-w-screen-2xl mx-auto">
          <div className="bg-surface-container-low rounded-[2.5rem] p-10 flex flex-wrap justify-between items-center gap-8 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-full node-edge-motif pointer-events-none" />
            {[
              { label: "Active Explorers", value: "1.2M+" },
              { label: "Global Nodes", value: "45.8K" },
              { label: "Success Rate", value: "99.4%" },
              { label: "Co2 Offset", value: "240T", green: true },
            ].map((stat) => (
              <div key={stat.label} className="flex-1 min-w-[180px]">
                <p className="text-sm font-bold text-outline uppercase tracking-[0.2em] mb-2 font-label">
                  {stat.label}
                </p>
                <h4
                  className={`text-5xl font-black font-headline ${
                    stat.green ? "text-secondary" : "text-on-surface"
                  }`}
                >
                  {stat.value}
                </h4>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Destinations */}
      <section className="px-6 mb-24">
        <div className="max-w-screen-2xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-end mb-12 gap-4">
            <div className="max-w-xl">
              <h2 className="text-4xl md:text-5xl font-black font-headline text-on-surface tracking-tight">
                Featured Destinations
              </h2>
              <p className="text-on-surface-variant mt-4 leading-relaxed">
                Dynamic nodes currently trending across the global graph.
              </p>
            </div>
            <Link
              to="/explore"
              className="flex items-center gap-2 text-primary font-bold hover:gap-4 transition-all"
            >
              View All{" "}
              <span className="material-symbols-outlined">arrow_forward</span>
            </Link>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div key={i} className="h-56 rounded-3xl bg-surface-container-low animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {featuredDestinations.map((destination) => (
                <DestinationCard
                  key={destination.id}
                  id={destination.id}
                  name={destination.name}
                  country={destination.country}
                  description={destination.description}
                  category={destination.category}
                  season={destination.season}
                />
              ))}
            </div>
          )}
        </div>
      </section>

      {/* CTA */}
      <section className="px-6 mb-24">
        <div className="max-w-screen-2xl mx-auto">
          <div className="bg-gradient-to-br from-primary to-primary-container rounded-3xl p-12 text-center relative overflow-hidden">
            <div className="absolute inset-0 node-edge-motif opacity-10" />
            <h2 className="text-4xl font-black font-headline text-on-primary mb-4 relative z-10">
              Ready to Map Your Journey?
            </h2>
            <p className="text-on-primary/80 max-w-lg mx-auto mb-8 relative z-10">
              Join 1.2M+ explorers navigating the world with intelligence.
            </p>
            <Link
              to="/register"
              className="inline-block px-10 py-4 bg-white text-primary font-bold rounded-lg shadow-xl hover:scale-105 transition-transform relative z-10"
            >
              Get Started Free
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="w-full rounded-t-3xl bg-surface-container-low">
        <div className="w-full py-12 px-8 flex flex-col md:flex-row justify-between items-center gap-6 max-w-screen-2xl mx-auto">
          <div className="flex flex-col gap-2">
            <span className="text-lg font-black text-on-surface font-headline">
              TravelGraph
            </span>
            <p className="text-xs text-outline">
              © 2024 TravelGraph. Mapping the world's possibilities.
            </p>
          </div>
          <div className="flex flex-wrap justify-center gap-8">
            {["Privacy Policy", "Terms of Service", "About"].map((link) => (
              <a
                key={link}
                href="#"
                className="text-xs text-outline hover:text-primary transition-colors"
              >
                {link}
              </a>
            ))}
          </div>
        </div>
      </footer>
    </div>
  );
}

export default HomePage;
