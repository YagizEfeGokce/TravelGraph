import apiClient from "./client";

type LoginPayload = {
  email: string;
  password: string;
};

type RegisterPayload = {
  name: string;
  email: string;
  password: string;
};

export async function loginUser(payload: LoginPayload) {
  const response = await apiClient.post("/auth/login", payload);
  return response.data;
}

export async function registerUser(payload: RegisterPayload) {
  const response = await apiClient.post("/auth/register", payload);
  return response.data;
}