import apiClient from "./client";

export async function getDestinations() {
  const response = await apiClient.get("/destinations");
  return response.data;
}

export async function getDestinationById(id: string) {
  const response = await apiClient.get(`/destinations/${id}`);
  return response.data;
}

export async function getDestinationRecommendations(id: string) {
  const response = await apiClient.get(`/destinations/${id}/recommendations`);
  return response.data;
}