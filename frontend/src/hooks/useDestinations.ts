import { useEffect, useState } from "react";
import { getDestinations } from "../api/destinations";

export function useDestinations() {
  const [destinations, setDestinations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getDestinations()
      .then((data) => {
        setDestinations(data);
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Unknown error");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return { destinations, loading, error };
}