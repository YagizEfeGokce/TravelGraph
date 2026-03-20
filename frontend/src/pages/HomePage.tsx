import DestinationCard from "../components/DestinationCard";

function HomePage() {
  const featuredDestinations = [
    {
      name: "İstanbul",
      country: "Turkey",
      description: "Historic landmarks, Bosphorus views and vibrant city life.",
      category: "Culture",
      season: "Spring",
    },
    {
      name: "Kapadokya",
      country: "Turkey",
      description: "Fairy chimneys, cave hotels and sunrise balloon tours.",
      category: "Nature",
      season: "Autumn",
    },
    {
      name: "Antalya",
      country: "Turkey",
      description: "Mediterranean beaches, resorts and sunny summer escapes.",
      category: "Beach",
      season: "Summer",
    },
    {
      name: "İzmir",
      country: "Turkey",
      description: "Coastal city energy, local food and relaxed Aegean lifestyle.",
      category: "City",
      season: "Summer",
    },
    {
      name: "Trabzon",
      country: "Turkey",
      description: "Green mountain landscapes, fresh air and Black Sea nature.",
      category: "Nature",
      season: "Spring",
    },
    {
      name: "Gaziantep",
      country: "Turkey",
      description: "World-famous cuisine, history and unforgettable local flavors.",
      category: "Food",
      season: "Winter",
    },
  ];

  return (
    <div style={{ minHeight: "100vh" }}>
      <section
        style={{
          maxWidth: "1280px",
          margin: "0 auto",
          padding: "72px 24px 36px",
        }}
      >
        <div
          style={{
            background:
              "linear-gradient(135deg, rgba(20,184,166,0.95), rgba(45,212,191,0.92))",
            borderRadius: "32px",
            padding: "70px 32px",
            textAlign: "center",
            color: "white",
            boxShadow: "0 18px 45px rgba(20,184,166,0.22)",
            border: "1px solid rgba(255,255,255,0.24)",
          }}
        >
          <h1
            style={{
              fontSize: "clamp(34px, 6vw, 60px)",
              margin: "0 0 16px 0",
              fontWeight: 800,
              lineHeight: 1.1,
              letterSpacing: "-0.02em",
            }}
          >
            Discover Beautiful Destinations Across Turkey
          </h1>

          <p
            style={{
              maxWidth: "760px",
              margin: "0 auto 30px",
              lineHeight: 1.7,
              fontSize: "17px",
              opacity: 0.96,
            }}
          >
            Explore cities, compare travel themes, plan routes, manage your
            budget and discover festivals through a clean and modern travel
            interface.
          </p>

          <div
            style={{
              maxWidth: "760px",
              margin: "0 auto",
              display: "flex",
              gap: "12px",
              justifyContent: "center",
              flexWrap: "wrap",
            }}
          >
            <input
              type="text"
              placeholder="Search destinations, cities or travel themes..."
              style={{
                flex: "1 1 380px",
                minWidth: "260px",
                padding: "16px 18px",
                borderRadius: "14px",
                border: "none",
                outline: "none",
                fontSize: "15px",
                boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
              }}
            />

            <button
              style={{
                background: "#0f766e",
                color: "white",
                border: "none",
                padding: "16px 22px",
                borderRadius: "14px",
                fontWeight: 700,
                cursor: "pointer",
                boxShadow: "0 8px 18px rgba(15,118,110,0.25)",
              }}
            >
              Search Now
            </button>
          </div>
        </div>
      </section>

      <section
        style={{
          maxWidth: "1280px",
          margin: "0 auto",
          padding: "18px 24px 70px",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "end",
            gap: "20px",
            flexWrap: "wrap",
            marginBottom: "24px",
          }}
        >
          <div>
            <p
              style={{
                margin: "0 0 6px 0",
                color: "#14b8a6",
                fontWeight: 700,
                fontSize: "14px",
              }}
            >
              POPULAR PICKS
            </p>
            <h2
              style={{
                margin: 0,
                fontSize: "34px",
                color: "#111827",
              }}
            >
              Featured Destinations
            </h2>
          </div>

          <p
            style={{
              margin: 0,
              color: "#6b7280",
              maxWidth: "520px",
              lineHeight: 1.6,
            }}
          >
            Discover some of the most well-known and visually rich travel spots
            in Turkey for culture, beach, nature and food experiences.
          </p>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
            gap: "22px",
          }}
        >
          {featuredDestinations.map((destination) => (
            <DestinationCard
              key={destination.name}
              name={destination.name}
              country={destination.country}
              description={destination.description}
              category={destination.category}
              season={destination.season}
            />
          ))}
        </div>
      </section>
    </div>
  );
}

export default HomePage;