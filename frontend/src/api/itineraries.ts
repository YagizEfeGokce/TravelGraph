import apiClient from "./client";

export async function getItineraries() {
  const response = await apiClient.get("/itineraries");
  return response.data;
}

export async function createItinerary(data: {
  title: string;
  start_date: string;
  end_date: string;
  is_public?: boolean;
}) {
  const response = await apiClient.post("/itineraries", data);
  return response.data;
}

export async function deleteItinerary(id: string) {
  await apiClient.delete(`/itineraries/${id}`);
}

export async function getStops(itineraryId: string) {
  const response = await apiClient.get(`/itineraries/${itineraryId}/stops`);
  return response.data;
}

export async function addStop(
  itineraryId: string,
  data: {
    destination_id: string;
    day_number: number;
    order: number;
    notes?: string;
  },
) {
  const response = await apiClient.post(`/itineraries/${itineraryId}/stops`, data);
  return response.data;
}

export async function deleteStop(itineraryId: string, stopId: string) {
  await apiClient.delete(`/itineraries/${itineraryId}/stops/${stopId}`);
}
