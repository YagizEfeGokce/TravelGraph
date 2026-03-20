import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { createReview } from "../api/reviews";

type Props = {
  targetId: string;
  targetType: "activity" | "accommodation" | "restaurant";
  onSuccess: () => void;
  onCancel: () => void;
};

function ReviewForm({ targetId, targetType, onSuccess, onCancel }: Props) {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  if (!user) {
    navigate(`/login?next=${window.location.pathname}`);
    return null;
  }

  async function handleSubmit() {
    if (!comment.trim()) {
      setError("Please write a comment.");
      return;
    }
    setSubmitting(true);
    setError("");
    try {
      await createReview({ target_id: targetId, target_type: targetType, rating, comment });
      onSuccess();
    } catch {
      setError("Could not submit review. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div
      style={{
        background: "#f8fafc",
        borderRadius: "12px",
        padding: "16px",
        border: "1px solid #e5e7eb",
        marginTop: "10px",
      }}
    >
      <h4 style={{ margin: "0 0 12px", color: "#1f2937" }}>Write a Review</h4>

      <div style={{ marginBottom: "10px" }}>
        <label style={{ display: "block", marginBottom: "6px", fontSize: "13px", fontWeight: 600 }}>
          Rating
        </label>
        <div style={{ display: "flex", gap: "6px" }}>
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              onClick={() => setRating(star)}
              style={{
                background: "none",
                border: "none",
                fontSize: "22px",
                cursor: "pointer",
                color: star <= rating ? "#f59e0b" : "#d1d5db",
                padding: "0",
              }}
            >
              ★
            </button>
          ))}
        </div>
      </div>

      <div style={{ marginBottom: "12px" }}>
        <label style={{ display: "block", marginBottom: "6px", fontSize: "13px", fontWeight: 600 }}>
          Comment
        </label>
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Share your experience..."
          rows={3}
          style={{
            width: "100%",
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #d1d5db",
            fontSize: "14px",
            resize: "vertical",
            boxSizing: "border-box",
          }}
        />
      </div>

      {error && (
        <p style={{ color: "#dc2626", fontSize: "13px", marginBottom: "10px" }}>{error}</p>
      )}

      <div style={{ display: "flex", gap: "8px" }}>
        <button
          onClick={handleSubmit}
          disabled={submitting}
          style={{
            background: "#14b8a6",
            color: "white",
            border: "none",
            padding: "8px 16px",
            borderRadius: "8px",
            fontWeight: 600,
            cursor: submitting ? "not-allowed" : "pointer",
            fontSize: "14px",
            opacity: submitting ? 0.7 : 1,
          }}
        >
          {submitting ? "Submitting..." : "Submit Review"}
        </button>
        <button
          onClick={onCancel}
          style={{
            background: "#e5e7eb",
            color: "#374151",
            border: "none",
            padding: "8px 16px",
            borderRadius: "8px",
            fontWeight: 600,
            cursor: "pointer",
            fontSize: "14px",
          }}
        >
          Cancel
        </button>
      </div>
    </div>
  );
}

export default ReviewForm;
