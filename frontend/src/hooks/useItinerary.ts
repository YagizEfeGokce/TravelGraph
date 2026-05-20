import { useEffect, useState } from "react";
import { getItineraries } from "../api/itineraries";

export function useItinerary() {
  const [itineraries, setItineraries] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getItineraries()
      .then((data) => {
        setItineraries(data);
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Unknown error");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return { itineraries, loading, error };
}