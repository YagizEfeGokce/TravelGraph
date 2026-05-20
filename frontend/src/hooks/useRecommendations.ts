import { useEffect, useState } from "react";
import { getDestinationRecommendations } from "../api/destinations";

export function useRecommendations(id: string) {
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getDestinationRecommendations(id)
      .then((data) => {
        setRecommendations(data);
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Unknown error");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [id]);

  return { recommendations, loading, error };
}