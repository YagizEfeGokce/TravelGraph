type StarRatingProps = {
  rating: number;
};

function StarRating({ rating }: StarRatingProps) {
  return (
    <div style={{ color: "#f59e0b", fontSize: "18px" }}>
      {"★".repeat(rating)}
      {"☆".repeat(5 - rating)}
    </div>
  );
}

export default StarRating;