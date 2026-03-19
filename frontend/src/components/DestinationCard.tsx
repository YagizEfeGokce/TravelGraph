import { Link } from "react-router-dom";

type DestinationCardProps = {
  name: string;
  country: string;
  description?: string;
  category?: string;
  season?: string;
};

function DestinationCard({
  name,
  country,
  description,
  category,
  season,
}: DestinationCardProps) {
  const slug = name.toLowerCase().replace(/\s+/g, "-");

  return (
    <Link
      to={`/destinations/${slug}`}
      style={{ textDecoration: "none", color: "inherit" }}
    >
      <div
        style={{
          background: "rgba(255,255,255,0.92)",
          backdropFilter: "blur(10px)",
          borderRadius: "22px",
          padding: "22px",
          boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
          border: "1px solid rgba(255,255,255,0.7)",
          transition: "transform 0.2s ease, box-shadow 0.2s ease",
          minHeight: "220px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
        }}
      >
        <div>
          <div
            style={{
              display: "inline-block",
              padding: "6px 12px",
              borderRadius: "999px",
              background: "rgba(20,184,166,0.12)",
              color: "#0f766e",
              fontSize: "12px",
              fontWeight: 700,
              marginBottom: "14px",
            }}
          >
            {country}
          </div>

          <h3
            style={{
              margin: "0 0 10px 0",
              fontSize: "24px",
              color: "#111827",
            }}
          >
            {name}
          </h3>

          <p
            style={{
              margin: 0,
              color: "#6b7280",
              lineHeight: 1.6,
              fontSize: "14px",
            }}
          >
            {description || "Explore local culture, food, activities and hidden gems."}
          </p>
        </div>

        <div style={{ marginTop: "18px" }}>
          <div
            style={{
              display: "flex",
              gap: "10px",
              flexWrap: "wrap",
              marginBottom: "16px",
            }}
          >
            {category && (
              <span
                style={{
                  padding: "6px 10px",
                  borderRadius: "999px",
                  background: "#ecfeff",
                  color: "#0f766e",
                  fontSize: "12px",
                  fontWeight: 600,
                }}
              >
                {category}
              </span>
            )}

            {season && (
              <span
                style={{
                  padding: "6px 10px",
                  borderRadius: "999px",
                  background: "#f0fdfa",
                  color: "#115e59",
                  fontSize: "12px",
                  fontWeight: 600,
                }}
              >
                Best in {season}
              </span>
            )}
          </div>

          <div
            style={{
              color: "#14b8a6",
              fontWeight: 700,
              fontSize: "14px",
            }}
          >
            View Details →
          </div>
        </div>
      </div>
    </Link>
  );
}

export default DestinationCard;