import apiClient from "./client";

export async function getReviews(destinationId: string) {
  const response = await apiClient.get(`/destinations/${destinationId}/reviews`);
  return response.data;
}

export async function createReview(data: any) {
  const response = await apiClient.post("/reviews", data);
  return response.data;
}