import apiClient from "./client";

type RegisterPayload = {
  name: string;
  email: string;
  password: string;
};

export async function loginUser({ email, password }: { email: string; password: string }) {
  // Backend uses OAuth2PasswordRequestForm — must send as form-encoded data
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await apiClient.post("/auth/login", formData, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return response.data; // { access_token, refresh_token, token_type, user }
}

export async function registerUser(payload: RegisterPayload) {
  const response = await apiClient.post("/auth/register", payload);
  return response.data; // { access_token, refresh_token, token_type, user }
}

export async function getMe() {
  const response = await apiClient.get("/auth/me");
  return response.data;
}
