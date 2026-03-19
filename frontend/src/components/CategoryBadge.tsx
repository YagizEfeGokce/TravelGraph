type CategoryBadgeProps = {
  category: string;
};

function CategoryBadge({ category }: CategoryBadgeProps) {
  return (
    <span
      style={{
        background: "#dcfce7",
        color: "#166534",
        padding: "4px 10px",
        borderRadius: "999px",
        fontSize: "12px",
        fontWeight: 600,
      }}
    >
      {category}
    </span>
  );
}

export default CategoryBadge;