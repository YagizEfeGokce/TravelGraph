import { useEffect, useState } from "react";
import { getDestinationRecommendations } from "../api/destinations";

export function useRecommendations(id: string) {
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDestinationRecommendations(id)
      .then((data) => {
        setRecommendations(data);
      })
      .catch(() => {})
      .finally(() => {
        setLoading(false);
      });
  }, [id]);

  return { recommendations, loading };
}