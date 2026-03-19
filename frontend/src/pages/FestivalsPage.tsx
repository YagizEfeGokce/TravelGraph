import { useMemo, useState } from "react";
import FestivalCard from "../components/FestivalCard";

function FestivalsPage() {
  const festivals = [
    { name: "Spring Music Fest", date: "2026-04-12", season: "Spring" },
    { name: "Food Carnival", date: "2026-05-03", season: "Spring" },
    { name: "Summer Beach Party", date: "2026-07-20", season: "Summer" },
    { name: "Autumn Art Fair", date: "2026-10-05", season: "Autumn" },
    { name: "Winter Lights Festival", date: "2026-12-18", season: "Winter" },
  ];

  const [selectedSeason, setSelectedSeason] = useState("All");
  const [searchText, setSearchText] = useState("");

  const filteredFestivals = useMemo(() => {
    return festivals.filter((festival) => {
      const matchesSeason =
        selectedSeason === "All" || festival.season === selectedSeason;

      const matchesSearch = festival.name
        .toLowerCase()
        .includes(searchText.toLowerCase());

      return matchesSeason && matchesSearch;
    });
  }, [festivals, searchText, selectedSeason]);

  return (
    <div style={{ padding: "40px", maxWidth: "1200px", margin: "0 auto" }}>
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ fontSize: "36px", marginBottom: "10px", color: "#1f2937" }}>
          Festival Calendar
        </h1>
        <p style={{ color: "#6b7280" }}>
          Explore seasonal festivals and discover upcoming local events.
        </p>
      </div>

      <div
        style={{
          display: "flex",
          gap: "16px",
          flexWrap: "wrap",
          marginBottom: "28px",
          background: "white",
          padding: "18px",
          borderRadius: "16px",
          boxShadow: "0 6px 16px rgba(0,0,0,0.06)",
        }}
      >
        <input
          type="text"
          placeholder="Search festival..."
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          style={{
            flex: "1 1 240px",
            padding: "12px 14px",
            border: "1px solid #d1d5db",
            borderRadius: "10px",
            fontSize: "15px",
          }}
        />

        <select
          value={selectedSeason}
          onChange={(e) => setSelectedSeason(e.target.value)}
          style={{
            padding: "12px 14px",
            border: "1px solid #d1d5db",
            borderRadius: "10px",
            fontSize: "15px",
            minWidth: "180px",
          }}
        >
          <option value="All">All Seasons</option>
          <option value="Spring">Spring</option>
          <option value="Summer">Summer</option>
          <option value="Autumn">Autumn</option>
          <option value="Winter">Winter</option>
        </select>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
          gap: "20px",
        }}
      >
        {filteredFestivals.map((festival) => (
          <FestivalCard
            key={festival.name}
            name={festival.name}
            date={festival.date}
            season={festival.season}
          />
        ))}
      </div>
    </div>
  );
}

export default FestivalsPage;