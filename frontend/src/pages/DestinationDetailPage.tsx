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
    <span style={{ color: "#f59e0b", fontSize: "15px" }}>
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
    <div style={{ marginTop: "12px" }}>
      {reviews.map((r) => (
        <div
          key={r.id}
          style={{
            background: "#f8fafc",
            borderRadius: "8px",
            padding: "10px 12px",
            marginBottom: "8px",
            border: "1px solid #e5e7eb",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
            <StarRow rating={r.rating} />
            <span style={{ fontWeight: 600, fontSize: "13px" }}>{r.user_name}</span>
            <span style={{ fontSize: "12px", color: "#9ca3af" }}>
              {new Date(r.created_at).toLocaleDateString()}
            </span>
          </div>
          <p style={{ margin: 0, fontSize: "13px", color: "#374151" }}>{r.comment}</p>
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
    <div style={{ marginTop: "8px" }}>
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
          style={{
            background: "none",
            border: "1px solid #14b8a6",
            color: "#14b8a6",
            padding: "6px 12px",
            borderRadius: "6px",
            cursor: "pointer",
            fontSize: "13px",
            fontWeight: 500,
            marginTop: "6px",
          }}
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
      <div style={{ padding: "60px", textAlign: "center", color: "#6b7280" }}>
        Loading...
      </div>
    );
  }

  if (error || !destination) {
    return (
      <div style={{ padding: "60px", textAlign: "center", color: "#dc2626" }}>
        {error || "Destination not found."}
      </div>
    );
  }

  const sectionTitle = (text: string) => (
    <h2
      style={{
        fontSize: "24px",
        fontWeight: 700,
        marginBottom: "16px",
        color: "#1f2937",
        borderBottom: "2px solid #f0fafa",
        paddingBottom: "8px",
      }}
    >
      {text}
    </h2>
  );

  const card = {
    background: "white",
    borderRadius: "14px",
    padding: "18px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.06)",
    border: "1px solid #e5e7eb",
  };

  const grid = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
    gap: "16px",
  };

  const priceLabel = (price: number) =>
    price === 0 ? "Free" : `₺${price.toFixed(0)}`;

  return (
    <div style={{ padding: "40px", maxWidth: "1100px", margin: "0 auto" }}>
      {/* Hero */}
      <section style={{ marginBottom: "40px" }}>
        <h1 style={{ fontSize: "40px", fontWeight: 800, marginBottom: "6px", color: "#1f2937" }}>
          {destination.name}
        </h1>
        <p style={{ color: "#14b8a6", fontWeight: 600, marginBottom: "10px" }}>
          {destination.country}
        </p>
        <p style={{ color: "#6b7280", lineHeight: 1.7, maxWidth: "700px" }}>
          {destination.description}
        </p>
      </section>

      {/* Activities */}
      {activities.length > 0 && (
        <section style={{ marginBottom: "40px" }}>
          {sectionTitle(`Activities (${activities.length})`)}
          <div style={grid}>
            {activities.map((act) => (
              <div key={act.id} style={card}>
                <h3 style={{ fontSize: "16px", fontWeight: 700, marginBottom: "6px" }}>
                  {act.name}
                </h3>
                <p style={{ fontSize: "13px", color: "#6b7280", marginBottom: "10px", lineHeight: 1.5 }}>
                  {act.description}
                </p>
                <div style={{ fontSize: "13px", color: "#374151", display: "flex", gap: "12px", flexWrap: "wrap" }}>
                  <span>⏱ {act.duration_hours}h</span>
                  <span>💰 {priceLabel(act.price)}</span>
                </div>
                {act.address && (
                  <p style={{ fontSize: "12px", color: "#9ca3af", marginTop: "6px" }}>
                    📍 {act.address}
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
        <section style={{ marginBottom: "40px" }}>
          {sectionTitle(`Restaurants (${restaurants.length})`)}
          <div style={grid}>
            {restaurants.map((r) => (
              <div key={r.id} style={card}>
                <h3 style={{ fontSize: "16px", fontWeight: 700, marginBottom: "6px" }}>
                  {r.name}
                </h3>
                <p style={{ fontSize: "13px", color: "#14b8a6", fontWeight: 600, marginBottom: "6px" }}>
                  {r.cuisine_type}
                </p>
                <div style={{ fontSize: "13px", color: "#374151", display: "flex", gap: "12px" }}>
                  <span style={{ textTransform: "capitalize" }}>💲 {r.price_range}</span>
                  {r.rating && <span>⭐ {r.rating.toFixed(1)}</span>}
                </div>
                {r.address && (
                  <p style={{ fontSize: "12px", color: "#9ca3af", marginTop: "6px" }}>
                    📍 {r.address}
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
        <section style={{ marginBottom: "40px" }}>
          {sectionTitle(`Where to Stay (${accommodations.length})`)}
          <div style={grid}>
            {accommodations.map((acc) => (
              <div key={acc.id} style={card}>
                <h3 style={{ fontSize: "16px", fontWeight: 700, marginBottom: "6px" }}>
                  {acc.name}
                </h3>
                <p style={{ fontSize: "13px", color: "#6b7280", marginBottom: "8px", textTransform: "capitalize" }}>
                  {acc.type.replace("_", " ")} {"★".repeat(acc.star_rating)}
                </p>
                <p style={{ fontSize: "15px", fontWeight: 700, color: "#14b8a6" }}>
                  ₺{acc.price_per_night.toFixed(0)} / night
                </p>
                {acc.address && (
                  <p style={{ fontSize: "12px", color: "#9ca3af", marginTop: "6px" }}>
                    📍 {acc.address}
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
        <section style={{ marginBottom: "40px" }}>
          {sectionTitle(`Festivals & Events (${festivals.length})`)}
          <div style={grid}>
            {festivals.map((f) => (
              <div key={f.id} style={card}>
                <h3 style={{ fontSize: "16px", fontWeight: 700, marginBottom: "6px" }}>
                  {f.name}
                </h3>
                <p style={{ fontSize: "13px", color: "#6b7280", marginBottom: "8px", lineHeight: 1.5 }}>
                  {f.description}
                </p>
                <p style={{ fontSize: "13px", color: "#374151" }}>
                  📅 {f.start_date} → {f.end_date}
                </p>
                {f.ticket_price != null && (
                  <p style={{ fontSize: "13px", color: "#374151", marginTop: "4px" }}>
                    🎟 {f.ticket_price === 0 ? "Free" : `₺${f.ticket_price}`}
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
          <p style={{ color: "#9ca3af", textAlign: "center", padding: "40px" }}>
            No details available for this destination yet.
          </p>
        )}
    </div>
  );
}

export default DestinationDetailPage;
