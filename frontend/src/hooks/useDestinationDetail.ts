import { useEffect, useState } from "react";
import { getDestinationById } from "../api/destinations";

export function useDestinationDetail(id: string) {
  const [destination, setDestination] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDestinationById(id)
      .then((data) => {
        setDestination(data);
      })
      .catch(() => {})
      .finally(() => {
        setLoading(false);
      });
  }, [id]);

  return { destination, loading };
}