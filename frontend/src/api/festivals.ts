import apiClient from "./client";

export async function getFestivals() {
  const response = await apiClient.get("/festivals");
  return response.data;
}

export async function getFestivalsBySeason(season: string) {
  const response = await apiClient.get(`/festivals?season=${season}`);
  return response.data;
}