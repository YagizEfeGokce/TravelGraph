type ActivityCardProps = {
  title: string;
  duration: string;
  price: string;
  category: string;
};

function ActivityCard({ title, duration, price, category }: ActivityCardProps) {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "14px",
        padding: "16px",
        boxShadow: "0 6px 16px rgba(0,0,0,0.08)",
      }}
    >
      <h3 style={{ marginBottom: "8px" }}>{title}</h3>
      <p>Duration: {duration}</p>
      <p>Price: {price}</p>
      <p>Category: {category}</p>
    </div>
  );
}

export default ActivityCard;