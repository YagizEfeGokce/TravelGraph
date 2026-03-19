type BudgetBreakdownProps = {
  accommodation: number;
  food: number;
  transport: number;
  activities: number;
};

function BudgetBreakdown({
  accommodation,
  food,
  transport,
  activities,
}: BudgetBreakdownProps) {
  const total = accommodation + food + transport + activities;

  return (
    <div
      style={{
        background: "white",
        padding: "20px",
        borderRadius: "14px",
        boxShadow: "0 6px 16px rgba(0,0,0,0.08)",
        marginTop: "20px",
      }}
    >
      <h3 style={{ marginBottom: "14px" }}>Budget Breakdown</h3>

      <p>Accommodation: €{accommodation}</p>
      <p>Food: €{food}</p>
      <p>Transport: €{transport}</p>
      <p>Activities: €{activities}</p>

      <hr />

      <strong>Total: €{total}</strong>
    </div>
  );
}

export default BudgetBreakdown;