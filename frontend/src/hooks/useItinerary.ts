import { useEffect, useState } from "react";
import { getItineraries } from "../api/itineraries";

export function useItinerary() {
  const [itineraries, setItineraries] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getItineraries()
      .then((data) => {
        setItineraries(data);
      })
      .catch(() => {})
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return { itineraries, loading };
}