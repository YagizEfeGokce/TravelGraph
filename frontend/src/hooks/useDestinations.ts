import { useEffect, useState } from "react";
import { getDestinations } from "../api/destinations";

export function useDestinations() {
  const [destinations, setDestinations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDestinations()
      .then((data) => {
        setDestinations(data);
      })
      .catch(() => {})
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return { destinations, loading };
}