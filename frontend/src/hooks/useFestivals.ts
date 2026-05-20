import { useEffect, useState } from "react";
import { getFestivals } from "../api/festivals";

export function useFestivals() {
  const [festivals, setFestivals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getFestivals()
      .then((data) => {
        setFestivals(data);
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Unknown error");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return { festivals, loading, error };
}