type RestaurantCardProps = {
  name: string;
  cuisine: string;
  priceRange: string;
};

function RestaurantCard({
  name,
  cuisine,
  priceRange,
}: RestaurantCardProps) {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "14px",
        padding: "16px",
        boxShadow: "0 6px 16px rgba(0,0,0,0.08)",
      }}
    >
      <h3 style={{ marginBottom: "8px" }}>{name}</h3>
      <p>Cuisine: {cuisine}</p>
      <p>Price Range: {priceRange}</p>
    </div>
  );
}

export default RestaurantCard;