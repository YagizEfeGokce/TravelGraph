type FestivalCardProps = {
  name: string;
  date: string;
  season: string;
};

function FestivalCard({ name, date, season }: FestivalCardProps) {
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
      <p>Date: {date}</p>
      <p>Season: {season}</p>
    </div>
  );
}

export default FestivalCard;