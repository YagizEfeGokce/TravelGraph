import apiClient from "./client";

export async function getFestivals(city?: string) {
  const params = city ? `?city=${encodeURIComponent(city)}` : "";
  const response = await apiClient.get(`/festivals${params}`);
  return response.data;
}
