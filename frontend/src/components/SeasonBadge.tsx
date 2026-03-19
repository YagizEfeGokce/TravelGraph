type SeasonBadgeProps = {
  season: string;
};

function SeasonBadge({ season }: SeasonBadgeProps) {
  return (
    <span
      style={{
        background: "#e0f2fe",
        color: "#0369a1",
        padding: "4px 10px",
        borderRadius: "999px",
        fontSize: "12px",
        fontWeight: 600,
      }}
    >
      {season}
    </span>
  );
}

export default SeasonBadge;