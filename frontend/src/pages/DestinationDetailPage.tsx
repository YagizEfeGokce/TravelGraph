import { useParams } from "react-router-dom";
import ActivityCard from "../components/ActivityCard";
import RestaurantCard from "../components/RestaurantCard";
import AccommodationCard from "../components/AccommodationCard";
import FestivalCard from "../components/FestivalCard";

function DestinationDetailPage() {
  const { id } = useParams();

  const destinationName = id
    ? id.charAt(0).toUpperCase() + id.slice(1)
    : "Destination";

  const activities = [
    {
      title: "City Walking Tour",
      duration: "2 hours",
      price: "€25",
      category: "Sightseeing",
    },
    {
      title: "Museum Visit",
      duration: "1.5 hours",
      price: "€18",
      category: "Culture",
    },
  ];

  const restaurants = [
    {
      name: "Sunset Bistro",
      cuisine: "Local",
      priceRange: "$$",
    },
    {
      name: "Green Garden",
      cuisine: "Mediterranean",
      priceRange: "$$$",
    },
  ];

  const accommodations = [
    {
      name: "Grand Hotel",
      price: "€120/night",
      stars: "4 stars",
    },
    {
      name: "City Stay",
      price: "€80/night",
      stars: "3 stars",
    },
  ];

  const festivals = [
    {
      name: "Spring Music Fest",
      date: "2026-04-12",
      season: "Spring",
    },
    {
      name: "Food Carnival",
      date: "2026-05-03",
      season: "Spring",
    },
  ];

  return (
    <div style={{ padding: "40px", maxWidth: "1100px", margin: "0 auto" }}>
      <section style={{ marginBottom: "32px" }}>
        <h1 style={{ fontSize: "36px", marginBottom: "8px" }}>
          {destinationName}
        </h1>
        <p style={{ color: "#666", marginBottom: "12px" }}>Sample Country</p>
        <p>This page shows activities, restaurants, accommodations and festivals.</p>
      </section>

      <section style={{ marginBottom: "32px" }}>
        <h2 style={{ marginBottom: "16px" }}>Activities</h2>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "16px",
          }}
        >
          {activities.map((activity) => (
            <ActivityCard
              key={activity.title}
              title={activity.title}
              duration={activity.duration}
              price={activity.price}
              category={activity.category}
            />
          ))}
        </div>
      </section>

      <section style={{ marginBottom: "32px" }}>
        <h2 style={{ marginBottom: "16px" }}>Restaurants</h2>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "16px",
          }}
        >
          {restaurants.map((restaurant) => (
            <RestaurantCard
              key={restaurant.name}
              name={restaurant.name}
              cuisine={restaurant.cuisine}
              priceRange={restaurant.priceRange}
            />
          ))}
        </div>
      </section>

      <section style={{ marginBottom: "32px" }}>
        <h2 style={{ marginBottom: "16px" }}>Accommodations</h2>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "16px",
          }}
        >
          {accommodations.map((hotel) => (
            <AccommodationCard
              key={hotel.name}
              name={hotel.name}
              price={hotel.price}
              stars={hotel.stars}
            />
          ))}
        </div>
      </section>

      <section>
        <h2 style={{ marginBottom: "16px" }}>Festivals</h2>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "16px",
          }}
        >
          {festivals.map((festival) => (
            <FestivalCard
              key={festival.name}
              name={festival.name}
              date={festival.date}
              season={festival.season}
            />
          ))}
        </div>
      </section>
    </div>
  );
}

export default DestinationDetailPage;