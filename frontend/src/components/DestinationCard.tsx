import { Link } from "react-router-dom";

type DestinationCardProps = {
  id: string;
  name: string;
  country: string;
  description?: string;
  category?: string;
  season?: string;
};

function DestinationCard({
  id,
  name,
  country,
  description,
  category,
  season,
}: DestinationCardProps) {
  return (
    <Link to={`/destinations/${id}`} className="block group">
      <div className="relative rounded-3xl overflow-hidden bg-surface-container-high border border-outline-variant/30 shadow-card hover:shadow-2xl transition-shadow min-h-[220px] flex flex-col justify-between p-6">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 to-secondary/10 opacity-60 group-hover:opacity-80 transition-opacity" />
        <div className="absolute inset-0 node-edge-motif pointer-events-none" />

        <div className="relative z-10">
          <span className="inline-block px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed text-[11px] font-bold tracking-widest uppercase mb-3 font-label">
            {country}
          </span>

          <h3 className="text-2xl font-black font-headline text-on-surface mb-2 tracking-tight">
            {name}
          </h3>

          <p className="text-sm text-on-surface-variant leading-relaxed">
            {description || "Explore local culture, food, activities and hidden gems."}
          </p>
        </div>

        <div className="relative z-10 mt-4">
          <div className="flex flex-wrap gap-2 mb-3">
            {category && (
              <span className="px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-bold">
                {category}
              </span>
            )}
            {season && (
              <span className="px-3 py-1 rounded-full bg-secondary/10 text-secondary text-xs font-bold">
                Best in {season}
              </span>
            )}
          </div>
          <div className="flex items-center gap-1 text-primary font-bold text-sm group-hover:gap-2 transition-all">
            View Details
            <span className="material-symbols-outlined text-base">arrow_forward</span>
          </div>
        </div>
      </div>
    </Link>
  );
}

export default DestinationCard;
