import axios from "axios";
import type {
  SessionStartRequest,
  SessionStartResponse,
  MessageRequest,
  MessageResponse,
  SessionEndResponse,
  Persona,
} from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "/api";

const api = axios.create({
  baseURL: API_BASE_URL,
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
    try {
      const response = await api.get<{ personas: Persona[] }>("/personas");
      return response.data.personas;
    } catch (error) {
      console.error("Error fetching personas:", error);
      return [];
    }
  },

  async getScoringCategories(): Promise<ScoringCategory[]> {
    try {
      const response = await api.get<{ categories: ScoringCategory[] }>("/scoring-categories");
      return response.data.categories;
    } catch (error) {
      console.error("Error fetching scoring categories:", error);
      // Return default categories as fallback
      return [
        { key: 'explanation_clarity', label: 'Explanation Clarity' },
        { key: 'patience_encouragement', label: 'Patience & Encouragement' },
        { key: 'active_questioning', label: 'Active Questioning' },
        { key: 'adaptability', label: 'Adaptability' },
        { key: 'mathematical_accuracy', label: 'Mathematical Accuracy' }
      ];
    }
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
