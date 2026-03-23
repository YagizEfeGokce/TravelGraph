import { Link } from "react-router-dom";

type DestinationCardProps = {
  id: string;
  name: string;
  country: string;
  description?: string;
  category?: string;
  season?: string;
  imageUrl?: string;
};

function DestinationCard({
  id,
  name,
  country,
  description,
  category,
  season,
  imageUrl,
}: DestinationCardProps) {
  return (
    <Link to={`/destinations/${id}`} className="block group">
      <div className="relative rounded-3xl overflow-hidden bg-surface-container-high border border-outline-variant/30 shadow-card hover:shadow-2xl transition-all hover:-translate-y-1 min-h-[260px] flex flex-col justify-between">
        {/* Image */}
        {imageUrl ? (
          <div className="relative h-40 overflow-hidden flex-shrink-0">
            <img
              src={imageUrl}
              alt={name}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
            <span className="absolute top-3 left-3 inline-block px-3 py-1 rounded-full bg-black/40 backdrop-blur text-white text-[11px] font-bold tracking-widest uppercase font-label border border-white/20">
              {country}
            </span>
          </div>
        ) : (
          <div className="relative h-40 overflow-hidden flex-shrink-0">
            <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-secondary/20" />
            <div className="absolute inset-0 node-edge-motif pointer-events-none" />
            <span className="absolute top-3 left-3 inline-block px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed text-[11px] font-bold tracking-widest uppercase font-label">
              {country}
            </span>
          </div>
        )}

        {/* Content */}
        <div className="p-5 flex flex-col flex-1">
          <h3 className="text-xl font-black font-headline text-on-surface mb-1 tracking-tight">
            {name}
          </h3>
          <p className="text-sm text-on-surface-variant leading-relaxed flex-1">
            {description || "Explore local culture, food, activities and hidden gems."}
          </p>

          <div className="mt-4">
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
      </div>
    </Link>
  );
}

export default DestinationCard;
