function ReviewForm() {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "14px",
        padding: "20px",
        boxShadow: "0 6px 16px rgba(0,0,0,0.08)",
      }}
    >
      <h3 style={{ marginBottom: "16px", color: "#1f2937" }}>Leave a Review</h3>

      <div style={{ marginBottom: "14px" }}>
        <label style={{ display: "block", marginBottom: "8px", fontWeight: 600 }}>
          Rating
        </label>
        <select
          style={{
            width: "100%",
            padding: "12px",
            borderRadius: "10px",
            border: "1px solid #d1d5db",
          }}
        >
          <option>5</option>
          <option>4</option>
          <option>3</option>
          <option>2</option>
          <option>1</option>
        </select>
      </div>

      <div style={{ marginBottom: "14px" }}>
        <label style={{ display: "block", marginBottom: "8px", fontWeight: 600 }}>
          Comment
        </label>
        <textarea
          placeholder="Write your review..."
          rows={4}
          style={{
            width: "100%",
            padding: "12px",
            borderRadius: "10px",
            border: "1px solid #d1d5db",
            resize: "vertical",
            boxSizing: "border-box",
          }}
        />
      </div>

      <button
        style={{
          background: "#14b8a6",
          color: "white",
          border: "none",
          padding: "12px 18px",
          borderRadius: "10px",
          fontWeight: 600,
          cursor: "pointer",
        }}
      >
        Submit Review
      </button>
    </div>
  );
}

export default ReviewForm;