import apiClient from "./client";

export async function getBudget(itineraryId: string) {
  const response = await apiClient.get(`/itineraries/${itineraryId}/budget`);
  return response.data;
}

export async function createBudget(itineraryId: string, data: {
  total_budget: number;
  currency: string;
  hotel_budget: number;
  food_budget: number;
  transport_budget: number;
  activity_budget: number;
}) {
  const response = await apiClient.post(`/itineraries/${itineraryId}/budget`, data);
  return response.data;
}

export async function updateBudget(itineraryId: string, data: {
  total_budget: number;
  currency: string;
  hotel_budget: number;
  food_budget: number;
  transport_budget: number;
  activity_budget: number;
}) {
  const response = await apiClient.put(`/itineraries/${itineraryId}/budget`, data);
  return response.data;
}
