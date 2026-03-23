import apiClient from "./client";

export async function getReviews(targetId: string, targetType: string) {
  const response = await apiClient.get(
    `/reviews?target_id=${encodeURIComponent(targetId)}&target_type=${encodeURIComponent(targetType)}`,
  );
  return Array.isArray(response.data) ? response.data : response.data.reviews ?? [];
}

export async function createReview(data: {
  target_id: string;
  target_type: string;
  rating: number;
  comment: string;
}) {
  const response = await apiClient.post("/reviews", data);
  return response.data;
}
