import { useMemo, useState } from "react";
import DestinationCard from "../components/DestinationCard";

function ExplorePage() {
  const destinations = [
    { name: "İstanbul", city: "İstanbul", category: "Culture", season: "Spring", description: "Historic mosques, Bosphorus views and endless city energy." },
    { name: "Ankara", city: "Ankara", category: "History", season: "Autumn", description: "Capital city with museums, memorials and political heritage." },
    { name: "İzmir", city: "İzmir", category: "City", season: "Summer", description: "Aegean lifestyle, sea breeze and vibrant coastal living." },
    { name: "Antalya", city: "Antalya", category: "Beach", season: "Summer", description: "Sunny beaches, resorts and perfect Mediterranean holidays." },
    { name: "Muğla", city: "Muğla", category: "Beach", season: "Summer", description: "Bodrum, Marmaris and turquoise bays for summer escapes." },
    { name: "Nevşehir", city: "Nevşehir", category: "Nature", season: "Autumn", description: "Fairy chimneys, cave hotels and balloon-filled skies." },
    { name: "Trabzon", city: "Trabzon", category: "Nature", season: "Spring", description: "Green plateaus, rain-kissed mountains and Black Sea beauty." },
    { name: "Bursa", city: "Bursa", category: "History", season: "Winter", description: "Ottoman heritage, thermal history and mountain views." },
    { name: "Çanakkale", city: "Çanakkale", category: "History", season: "Spring", description: "Gallipoli history and routes filled with meaning." },
    { name: "Mardin", city: "Mardin", category: "Culture", season: "Autumn", description: "Stone architecture, local heritage and Mesopotamian views." },
    { name: "Gaziantep", city: "Gaziantep", category: "Food", season: "Winter", description: "Baklava, kebab and one of Turkey’s richest food scenes." },
    { name: "Eskişehir", city: "Eskişehir", category: "City", season: "Spring", description: "Student city charm, canals and modern social life." },
    { name: "Rize", city: "Rize", category: "Nature", season: "Summer", description: "Tea gardens, lush forests and cool mountain air." },
    { name: "Aydın", city: "Aydın", category: "Beach", season: "Summer", description: "Aegean beaches, warm weather and relaxed coastal vibes." },
    { name: "Şanlıurfa", city: "Şanlıurfa", category: "Culture", season: "Autumn", description: "Sacred history, ancient sites and deep cultural roots." },
    { name: "Konya", city: "Konya", category: "Culture", season: "Winter", description: "Spiritual heritage, Mevlana and calm cultural atmosphere." },
    { name: "Kayseri", city: "Kayseri", category: "History", season: "Winter", description: "Traditional food, Erciyes mountain and central Anatolian history." },
    { name: "Adana", city: "Adana", category: "Food", season: "Spring", description: "Famous cuisine, bold flavors and lively southern energy." },
    { name: "Samsun", city: "Samsun", category: "City", season: "Summer", description: "Coastal Black Sea city with parks and urban comfort." },
    { name: "Balıkesir", city: "Balıkesir", category: "Beach", season: "Summer", description: "Ayvalık coastlines and island-style seaside escapes." },
    { name: "Denizli", city: "Denizli", category: "Nature", season: "Spring", description: "Pamukkale terraces and world-famous thermal landscapes." },
    { name: "Kastamonu", city: "Kastamonu", category: "Nature", season: "Autumn", description: "Forests, canyons and underrated northern beauty." },
    { name: "Van", city: "Van", category: "Nature", season: "Summer", description: "Lake views, island church and eastern Anatolian scenery." },
    { name: "Artvin", city: "Artvin", category: "Nature", season: "Summer", description: "High mountains, green valleys and trekking routes." },
    { name: "Bolu", city: "Bolu", category: "Nature", season: "Winter", description: "Abant, forest retreats and peaceful seasonal escapes." },
    { name: "Kars", city: "Kars", category: "History", season: "Winter", description: "Snowy landscapes, Ani ruins and eastern frontier history." },
    { name: "Edirne", city: "Edirne", category: "History", season: "Spring", description: "Ottoman monuments and cultural gateway to Europe." },
    { name: "Hatay", city: "Hatay", category: "Food", season: "Spring", description: "Unique flavors, multicultural heritage and warm hospitality." },
    { name: "Ordu", city: "Ordu", category: "Nature", season: "Summer", description: "Black Sea coast, cable car views and green hills." },
    { name: "Sinop", city: "Sinop", category: "Beach", season: "Summer", description: "Quiet coastal charm and northern seaside beauty." },
    { name: "Fethiye", city: "Muğla", category: "Beach", season: "Summer", description: "Blue Lagoon, boat tours and postcard-perfect beaches." },
    { name: "Bodrum", city: "Muğla", category: "Beach", season: "Summer", description: "Luxury coastal vibe, nightlife and sea-view escapes." },
    { name: "Marmaris", city: "Muğla", category: "Beach", season: "Summer", description: "Marina life, beaches and classic holiday atmosphere." },
    { name: "Kuşadası", city: "Aydın", category: "Beach", season: "Summer", description: "Cruise stop, beaches and access to ancient ruins." },
    { name: "Safranbolu", city: "Karabük", category: "History", season: "Autumn", description: "Historic Ottoman houses and timeless town streets." },
    { name: "Amasya", city: "Amasya", category: "History", season: "Spring", description: "Riverside old town and royal tombs in the cliffs." },
    { name: "Uzungöl", city: "Trabzon", category: "Nature", season: "Summer", description: "Lake views, misty mountains and green tranquility." },
    { name: "Alaçatı", city: "İzmir", category: "Beach", season: "Summer", description: "Windy streets, stone houses and boutique summer energy." },
    { name: "Kaş", city: "Antalya", category: "Beach", season: "Summer", description: "Diving spots, calm sea and boutique holiday mood." },
    { name: "Side", city: "Antalya", category: "History", season: "Summer", description: "Ancient ruins mixed with resort-style beach travel." },
  ];

  const [category, setCategory] = useState("All");
  const [season, setSeason] = useState("All");
  const [city, setCity] = useState("All");

  const filteredDestinations = useMemo(() => {
    return destinations.filter((dest) => {
      const categoryMatch = category === "All" || dest.category === category;
      const seasonMatch = season === "All" || dest.season === season;
      const cityMatch = city === "All" || dest.city === city;

      return categoryMatch && seasonMatch && cityMatch;
    });
  }, [category, season, city]);

  return (
    <div style={{ maxWidth: "1280px", margin: "0 auto", padding: "40px 20px 70px" }}>
      <div style={{ marginBottom: "28px" }}>
        <p
          style={{
            margin: "0 0 8px 0",
            color: "#14b8a6",
            fontWeight: 700,
            fontSize: "14px",
          }}
        >
          DESTINATION DISCOVERY
        </p>

        <h1 style={{ fontSize: "38px", margin: "0 0 10px 0", color: "#111827" }}>
          Explore Destinations
        </h1>

        <p style={{ color: "#6b7280", maxWidth: "760px", lineHeight: 1.7 }}>
          Filter destinations across Turkey by travel category, best season and
          city to discover the places that fit your travel style.
        </p>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
          gap: "16px",
          marginBottom: "24px",
          background: "rgba(255,255,255,0.88)",
          backdropFilter: "blur(10px)",
          padding: "22px",
          borderRadius: "22px",
          boxShadow: "0 10px 24px rgba(0,0,0,0.05)",
          border: "1px solid rgba(255,255,255,0.7)",
        }}
      >
        <div>
          <label style={{ fontWeight: 700, color: "#374151" }}>Category</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            style={{
              width: "100%",
              padding: "12px",
              marginTop: "8px",
              borderRadius: "12px",
              border: "1px solid #d1d5db",
              background: "white",
            }}
          >
            <option>All</option>
            <option>Culture</option>
            <option>History</option>
            <option>Beach</option>
            <option>Nature</option>
            <option>Food</option>
            <option>City</option>
          </select>
        </div>

        <div>
          <label style={{ fontWeight: 700, color: "#374151" }}>Season</label>
          <select
            value={season}
            onChange={(e) => setSeason(e.target.value)}
            style={{
              width: "100%",
              padding: "12px",
              marginTop: "8px",
              borderRadius: "12px",
              border: "1px solid #d1d5db",
              background: "white",
            }}
          >
            <option>All</option>
            <option>Spring</option>
            <option>Summer</option>
            <option>Autumn</option>
            <option>Winter</option>
          </select>
        </div>

        <div>
          <label style={{ fontWeight: 700, color: "#374151" }}>City</label>
          <select
            value={city}
            onChange={(e) => setCity(e.target.value)}
            style={{
              width: "100%",
              padding: "12px",
              marginTop: "8px",
              borderRadius: "12px",
              border: "1px solid #d1d5db",
              background: "white",
            }}
          >
            <option>All</option>
            <option>İstanbul</option>
            <option>Ankara</option>
            <option>İzmir</option>
            <option>Antalya</option>
            <option>Muğla</option>
            <option>Nevşehir</option>
            <option>Trabzon</option>
            <option>Bursa</option>
            <option>Çanakkale</option>
            <option>Mardin</option>
            <option>Gaziantep</option>
            <option>Eskişehir</option>
            <option>Rize</option>
            <option>Aydın</option>
            <option>Şanlıurfa</option>
            <option>Konya</option>
            <option>Kayseri</option>
            <option>Adana</option>
            <option>Samsun</option>
            <option>Balıkesir</option>
            <option>Denizli</option>
            <option>Kastamonu</option>
            <option>Van</option>
            <option>Artvin</option>
            <option>Bolu</option>
            <option>Kars</option>
            <option>Edirne</option>
            <option>Hatay</option>
            <option>Ordu</option>
            <option>Sinop</option>
            <option>Karabük</option>
          </select>
        </div>
      </div>

      <div
        style={{
          marginBottom: "24px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: "14px",
          flexWrap: "wrap",
        }}
      >
        <div
          style={{
            background: "rgba(20,184,166,0.1)",
            color: "#0f766e",
            padding: "10px 16px",
            borderRadius: "999px",
            fontWeight: 700,
            fontSize: "14px",
          }}
        >
          {filteredDestinations.length} destinations found
        </div>

        <p style={{ margin: 0, color: "#6b7280", fontSize: "14px" }}>
          Filter results update instantly according to your selection.
        </p>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))",
          gap: "22px",
        }}
      >
        {filteredDestinations.map((dest) => (
          <DestinationCard
            key={dest.name}
            name={dest.name}
            country="Turkey"
            description={dest.description}
            category={dest.category}
            season={dest.season}
          />
        ))}
      </div>
    </div>
  );
}

export default ExplorePage;