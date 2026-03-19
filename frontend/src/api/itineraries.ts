import apiClient from "./client";

export async function getItineraries() {
  const response = await apiClient.get("/itineraries");
  return response.data;
}

export async function createItinerary(data: any) {
  const response = await apiClient.post("/itineraries", data);
  return response.data;
}