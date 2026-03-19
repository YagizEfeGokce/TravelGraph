type TagBadgeProps = {
  tag: string;
};

function TagBadge({ tag }: TagBadgeProps) {
  return (
    <span
      style={{
        background: "#fef3c7",
        color: "#92400e",
        padding: "4px 10px",
        borderRadius: "999px",
        fontSize: "12px",
        fontWeight: 600,
      }}
    >
      {tag}
    </span>
  );
}

export default TagBadge;