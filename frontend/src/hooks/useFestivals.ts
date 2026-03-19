import { useEffect, useState } from "react";
import { getFestivals } from "../api/festivals";

export function useFestivals() {
  const [festivals, setFestivals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getFestivals()
      .then((data) => {
        setFestivals(data);
      })
      .catch(() => {})
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return { festivals, loading };
}