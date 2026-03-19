function ProfilePage() {
  const trips = [
    "Paris Spring Trip",
    "Rome Weekend Plan",
    "Tokyo Food Tour",
  ];

  const savedPlans = [
    "Summer Europe Route",
    "Winter Japan Budget",
    "Beach Escape Plan",
  ];

  const reviews = [
    "Amazing city experience!",
    "Loved the local restaurants.",
    "Great place for a weekend trip.",
  ];

  return (
    <div
      style={{
        maxWidth: "1100px",
        margin: "0 auto",
        padding: "40px 20px",
      }}
    >
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ fontSize: "36px", marginBottom: "10px", color: "#1f2937" }}>
          Profile
        </h1>
        <p style={{ color: "#6b7280" }}>
          View your past trips, saved plans, and reviews.
        </p>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: "20px",
        }}
      >
        <ProfileCard title="Past Trips" items={trips} />
        <ProfileCard title="Saved Plans" items={savedPlans} />
        <ProfileCard title="Your Reviews" items={reviews} />
      </div>
    </div>
  );
}

type ProfileCardProps = {
  title: string;
  items: string[];
};

function ProfileCard({ title, items }: ProfileCardProps) {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "18px",
        padding: "24px",
        boxShadow: "0 8px 18px rgba(0,0,0,0.06)",
      }}
    >
      <h2 style={{ marginBottom: "16px", color: "#1f2937" }}>{title}</h2>

      <ul style={{ paddingLeft: "20px", color: "#374151", margin: 0 }}>
        {items.map((item) => (
          <li key={item} style={{ marginBottom: "10px" }}>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProfilePage;