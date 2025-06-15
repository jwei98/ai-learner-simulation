export type PersonaType = string;

export interface Persona {
  id: string;
  name: string;
}

export interface PersonaInfo {
  name: string;
  type: PersonaType;
  description: string;
}

export interface Message {
  id: string;
  content: string;
  sender: 'tutor' | 'learner';
  timestamp: string;
}

export interface Session {
  id: string;
  tutorName: string;
  problem: string;
  personaType: PersonaType;
  messages: Message[];
  isActive: boolean;
  createdAt: string;
  endedAt?: string;
}

export interface SessionStartRequest {
  tutor_name: string;
  problem: string;
  persona_type: PersonaType;
}

export interface SessionStartResponse {
  session_id: string;
  initial_response: string;
  persona_info: {
    name: string;
    type: string;
  };
}

export interface MessageRequest {
  message: string;
  sender: 'tutor' | 'learner';
}

export interface MessageResponse {
  response: string;
  session_active: boolean;
}

export interface CategoryScore {
  score: number;
  feedback: string;
}

export interface SessionEndResponse {
  categories: {
    explanation_clarity: CategoryScore;
    patience_encouragement: CategoryScore;
    active_questioning: CategoryScore;
    adaptability: CategoryScore;
    mathematical_accuracy: CategoryScore;
  };
  session_summary: string;
}

