type AccommodationCardProps = {
  name: string;
  price: string;
  stars: string;
};

function AccommodationCard({
  name,
  price,
  stars,
}: AccommodationCardProps) {
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
      <p>Price: {price}</p>
      <p>Stars: {stars}</p>
    </div>
  );
}

export default AccommodationCard;