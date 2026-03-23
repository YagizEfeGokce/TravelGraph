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
    <div className="bg-surface-container-low rounded-2xl p-4 border border-outline-variant/30 mt-3">
      <h4 className="font-black font-headline text-on-surface text-sm mb-4">Write a Review</h4>

      <div className="mb-4">
        <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
          Rating
        </label>
        <div className="flex gap-1">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              onClick={() => setRating(star)}
              className={`text-2xl p-0 bg-transparent border-none cursor-pointer transition-colors ${
                star <= rating ? "text-amber-400" : "text-outline-variant"
              }`}
            >
              ★
            </button>
          ))}
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
          Comment
        </label>
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Share your experience..."
          rows={3}
          className="w-full px-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm resize-vertical focus:outline-none focus:border-primary transition-colors placeholder:text-outline"
        />
      </div>

      {error && (
        <p className="text-error text-xs mb-3 font-medium">{error}</p>
      )}

      <div className="flex gap-2">
        <button
          onClick={handleSubmit}
          disabled={submitting}
          className="px-4 py-2 bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold rounded-lg text-sm hover:opacity-90 transition-all disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {submitting ? "Submitting..." : "Submit Review"}
        </button>
        <button
          onClick={onCancel}
          className="px-4 py-2 bg-surface-container text-on-surface-variant font-bold rounded-lg text-sm hover:bg-surface-container-high transition-colors"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}

export default ReviewForm;
