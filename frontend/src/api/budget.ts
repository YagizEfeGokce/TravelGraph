import apiClient from "./client";

export async function getBudget(planId: string) {
  const response = await apiClient.get(`/budgets/${planId}`);
  return response.data;
}

export async function createBudget(data: any) {
  const response = await apiClient.post("/budgets", data);
  return response.data;
}