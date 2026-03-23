import { useState, useEffect, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import apiClient from "../api/client";
import { getReviews } from "../api/reviews";
import ReviewForm from "../components/ReviewForm";

type Destination = {
  id: string;
  name: string;
  country: string;
  description: string;
};

type Activity = {
  id: string;
  name: string;
  description: string;
  duration_hours: number;
  price: number;
  address: string;
};

type Restaurant = {
  id: string;
  name: string;
  cuisine_type: string;
  price_range: string;
  address: string;
  rating?: number;
};

type Accommodation = {
  id: string;
  name: string;
  type: string;
  star_rating: number;
  price_per_night: number;
  address: string;
};

type Festival = {
  id: string;
  name: string;
  description: string;
  start_date: string;
  end_date: string;
  ticket_price?: number;
};

type Review = {
  id: string;
  rating: number;
  comment: string;
  user_name: string;
  created_at: string;
};

function StarRow({ rating }: { rating: number }) {
  return (
    <span className="text-amber-400 text-sm">
      {"★".repeat(rating)}{"☆".repeat(5 - rating)}
    </span>
  );
}

function ReviewList({
  targetId,
  targetType,
  refreshKey,
}: {
  targetId: string;
  targetType: string;
  refreshKey: number;
}) {
  const [reviews, setReviews] = useState<Review[]>([]);

  useEffect(() => {
    getReviews(targetId, targetType)
      .then(setReviews)
      .catch(() => {});
  }, [targetId, targetType, refreshKey]);

  if (reviews.length === 0) return null;

  return (
    <div className="mt-3 space-y-2">
      {reviews.map((r) => (
        <div
          key={r.id}
          className="bg-surface-container-low rounded-xl px-4 py-3 border border-outline-variant/20"
        >
          <div className="flex items-center gap-2 mb-1">
            <StarRow rating={r.rating} />
            <span className="font-bold text-xs text-on-surface">{r.user_name}</span>
            <span className="text-xs text-outline">
              {new Date(r.created_at).toLocaleDateString()}
            </span>
          </div>
          <p className="text-sm text-on-surface-variant">{r.comment}</p>
        </div>
      ))}
    </div>
  );
}

type ItemType = "activity" | "accommodation" | "restaurant";

function ReviewSection({
  item,
  type,
}: {
  item: { id: string };
  type: ItemType;
}) {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [showForm, setShowForm] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  function handleWriteReview() {
    if (!user) {
      navigate(`/login?next=${window.location.pathname}`);
      return;
    }
    setShowForm(true);
  }

  return (
    <div className="mt-3">
      <ReviewList targetId={item.id} targetType={type} refreshKey={refreshKey} />
      {showForm ? (
        <ReviewForm
          targetId={item.id}
          targetType={type}
          onSuccess={() => {
            setShowForm(false);
            setRefreshKey((k) => k + 1);
          }}
          onCancel={() => setShowForm(false)}
        />
      ) : (
        <button
          onClick={handleWriteReview}
          className="mt-2 px-3 py-1.5 text-xs font-bold text-primary border border-primary/30 rounded-lg hover:bg-primary/5 transition-colors"
        >
          Write a Review
        </button>
      )}
    </div>
  );
}

function DestinationDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [destination, setDestination] = useState<Destination | null>(null);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [accommodations, setAccommodations] = useState<Accommodation[]>([]);
  const [festivals, setFestivals] = useState<Festival[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchAll = useCallback(async () => {
    if (!id) return;
    setLoading(true);
    try {
      const [dest, acts, rests, accs, fests] = await Promise.all([
        apiClient.get(`/destinations/${id}`),
        apiClient.get(`/destinations/${id}/activities`),
        apiClient.get(`/destinations/${id}/restaurants`),
        apiClient.get(`/destinations/${id}/accommodations`),
        apiClient.get(`/destinations/${id}/festivals`),
      ]);
      setDestination(dest.data);
      setActivities(acts.data);
      setRestaurants(rests.data);
      setAccommodations(accs.data);
      setFestivals(fests.data);
    } catch {
      setError("Could not load destination details.");
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchAll();
  }, [fetchAll]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center pt-24">
        <div className="text-center">
          <div className="w-12 h-12 rounded-full border-4 border-primary border-t-transparent animate-spin mx-auto mb-4" />
          <p className="text-on-surface-variant font-medium">Loading destination...</p>
        </div>
      </div>
    );
  }

  if (error || !destination) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center pt-24">
        <div className="text-center">
          <p className="text-error font-medium text-lg">{error || "Destination not found."}</p>
        </div>
      </div>
    );
  }

  const priceLabel = (price: number) =>
    price === 0 ? "Free" : `₺${price.toFixed(0)}`;

  const SectionTitle = ({ text }: { text: string }) => (
    <h2 className="text-2xl font-black font-headline text-on-surface tracking-tight mb-6 pb-2 border-b border-outline-variant/30">
      {text}
    </h2>
  );

  return (
    <div className="bg-background min-h-screen pt-24 pb-16 px-6">
      <div className="max-w-screen-xl mx-auto">
        {/* Hero */}
        <section className="mb-12">
          <div className="relative rounded-3xl overflow-hidden bg-surface-container-high p-10 border border-outline-variant/20 shadow-ambient">
            <div className="absolute inset-0 bg-gradient-to-br from-primary/10 to-secondary/10" />
            <div className="absolute inset-0 node-edge-motif pointer-events-none" />
            <div className="relative z-10">
              <span className="inline-block px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed text-[10px] font-bold tracking-widest uppercase mb-4 font-label">
                {destination.country}
              </span>
              <h1 className="text-5xl md:text-7xl font-black font-headline text-on-surface tracking-tight mb-4">
                {destination.name}
              </h1>
              <p className="text-on-surface-variant leading-relaxed max-w-2xl text-lg">
                {destination.description}
              </p>
            </div>
          </div>
        </section>

        {/* Activities */}
        {activities.length > 0 && (
          <section className="mb-12">
            <SectionTitle text={`Activities (${activities.length})`} />
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {activities.map((act) => (
                <div
                  key={act.id}
                  className="bg-surface-container-lowest rounded-2xl p-5 border border-outline-variant/30 shadow-card"
                >
                  <h3 className="font-black font-headline text-on-surface text-base mb-2">
                    {act.name}
                  </h3>
                  <p className="text-sm text-on-surface-variant leading-relaxed mb-3">
                    {act.description}
                  </p>
                  <div className="flex flex-wrap gap-3 text-xs font-bold mb-2">
                    <span className="px-2 py-1 rounded-lg bg-surface-container text-on-surface-variant">
                      {act.duration_hours}h
                    </span>
                    <span className="px-2 py-1 rounded-lg bg-primary/10 text-primary">
                      {priceLabel(act.price)}
                    </span>
                  </div>
                  {act.address && (
                    <p className="text-xs text-outline mt-1 flex items-center gap-1">
                      <span className="material-symbols-outlined text-xs">location_on</span>
                      {act.address}
                    </p>
                  )}
                  <ReviewSection item={act} type="activity" />
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Restaurants */}
        {restaurants.length > 0 && (
          <section className="mb-12">
            <SectionTitle text={`Restaurants (${restaurants.length})`} />
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {restaurants.map((r) => (
                <div
                  key={r.id}
                  className="bg-surface-container-lowest rounded-2xl p-5 border border-outline-variant/30 shadow-card"
                >
                  <h3 className="font-black font-headline text-on-surface text-base mb-1">
                    {r.name}
                  </h3>
                  <p className="text-sm font-bold text-secondary mb-2">{r.cuisine_type}</p>
                  <div className="flex flex-wrap gap-3 text-xs font-bold mb-2">
                    <span className="px-2 py-1 rounded-lg bg-surface-container text-on-surface-variant capitalize">
                      {r.price_range}
                    </span>
                    {r.rating && (
                      <span className="px-2 py-1 rounded-lg bg-amber-50 text-amber-700">
                        ★ {r.rating.toFixed(1)}
                      </span>
                    )}
                  </div>
                  {r.address && (
                    <p className="text-xs text-outline flex items-center gap-1">
                      <span className="material-symbols-outlined text-xs">location_on</span>
                      {r.address}
                    </p>
                  )}
                  <ReviewSection item={r} type="restaurant" />
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Accommodations */}
        {accommodations.length > 0 && (
          <section className="mb-12">
            <SectionTitle text={`Where to Stay (${accommodations.length})`} />
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {accommodations.map((acc) => (
                <div
                  key={acc.id}
                  className="bg-surface-container-lowest rounded-2xl p-5 border border-outline-variant/30 shadow-card"
                >
                  <h3 className="font-black font-headline text-on-surface text-base mb-1">
                    {acc.name}
                  </h3>
                  <p className="text-sm text-on-surface-variant mb-2 capitalize">
                    {acc.type.replace("_", " ")} {"★".repeat(acc.star_rating)}
                  </p>
                  <p className="text-lg font-black text-primary font-headline">
                    ₺{acc.price_per_night.toFixed(0)}{" "}
                    <span className="text-sm font-normal text-on-surface-variant">/ night</span>
                  </p>
                  {acc.address && (
                    <p className="text-xs text-outline mt-2 flex items-center gap-1">
                      <span className="material-symbols-outlined text-xs">location_on</span>
                      {acc.address}
                    </p>
                  )}
                  <ReviewSection item={acc} type="accommodation" />
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Festivals */}
        {festivals.length > 0 && (
          <section className="mb-12">
            <SectionTitle text={`Festivals & Events (${festivals.length})`} />
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {festivals.map((f) => (
                <div
                  key={f.id}
                  className="bg-surface-container-lowest rounded-2xl p-5 border border-outline-variant/30 shadow-card"
                >
                  <h3 className="font-black font-headline text-on-surface text-base mb-2">
                    {f.name}
                  </h3>
                  <p className="text-sm text-on-surface-variant leading-relaxed mb-3">
                    {f.description}
                  </p>
                  <p className="text-xs text-on-surface-variant flex items-center gap-1 mb-1">
                    <span className="material-symbols-outlined text-xs text-primary">calendar_month</span>
                    {f.start_date} → {f.end_date}
                  </p>
                  {f.ticket_price != null && (
                    <p className="text-xs font-bold text-primary">
                      {f.ticket_price === 0 ? "Free entry" : `₺${f.ticket_price}`}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {activities.length === 0 &&
          restaurants.length === 0 &&
          accommodations.length === 0 && (
            <div className="text-center py-20 text-on-surface-variant">
              <p className="text-lg font-medium">No details available for this destination yet.</p>
            </div>
          )}
      </div>
    </div>
  );
}

export default DestinationDetailPage;
