import axios from "axios";
import type {
  SessionStartRequest,
  SessionStartResponse,
  MessageRequest,
  MessageResponse,
  SessionEndResponse,
  Persona,
} from "../types";

const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export interface ScoringCategory {
  key: string;
  label: string;
  description?: string;
}

export const sessionApi = {
  async startSession(data: SessionStartRequest): Promise<SessionStartResponse> {
    const response = await api.post<SessionStartResponse>(
      "/sessions/start",
      data
    );
    return response.data;
  },

  async sendMessage(
    sessionId: string,
    message: MessageRequest
  ): Promise<MessageResponse> {
    const response = await api.post<MessageResponse>(
      `/sessions/${sessionId}/message`,
      message
    );
    return response.data;
  },

  async endSession(sessionId: string): Promise<SessionEndResponse> {
    const response = await api.post<SessionEndResponse>(
      `/sessions/${sessionId}/end`
    );
    return response.data;
  },

  async getPersonas(): Promise<Persona[]> {
    console.log("env", import.meta.env);
    const response = await api.get<{ personas: Persona[] }>("/personas");
    return response.data.personas;
  },

  async getScoringCategories(): Promise<ScoringCategory[]> {
    const response = await api.get<{ categories: ScoringCategory[] }>(
      "/scoring-categories"
    );
    return response.data.categories;
  },
};

// Error handling interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      console.error("API Error:", error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error("Network Error:", error.request);
    } else {
      // Something else happened
      console.error("Error:", error.message);
    }
    return Promise.reject(error);
  }
);
