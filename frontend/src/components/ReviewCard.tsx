import StarRating from "./StarRating";

type ReviewCardProps = {
  user: string;
  rating: number;
  comment: string;
};

function ReviewCard({ user, rating, comment }: ReviewCardProps) {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "14px",
        padding: "18px",
        boxShadow: "0 6px 16px rgba(0,0,0,0.08)",
      }}
    >
      <h3 style={{ marginBottom: "8px", color: "#1f2937" }}>{user}</h3>
      <div style={{ marginBottom: "10px" }}>
        <StarRating rating={rating} />
      </div>
      <p style={{ color: "#4b5563", margin: 0 }}>{comment}</p>
    </div>
  );
}

export default ReviewCard;