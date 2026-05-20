import { useEffect, useState } from "react";
import { getDestinationById } from "../api/destinations";

export function useDestinationDetail(id: string) {
  const [destination, setDestination] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getDestinationById(id)
      .then((data) => {
        setDestination(data);
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Unknown error");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [id]);

  return { destination, loading, error };
}