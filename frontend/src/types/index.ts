export type PersonaType = 
  | 'struggling_sam' 
  | 'overconfident_olivia' 
  | 'anxious_alex' 
  | 'methodical_maya';

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
  mathProblem: string;
  personaType: PersonaType;
  messages: Message[];
  isActive: boolean;
  createdAt: string;
  endedAt?: string;
}

export interface SessionStartRequest {
  tutor_name: string;
  math_problem: string;
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

export interface Scores {
  explanation_clarity: number;
  patience_encouragement: number;
  active_questioning: number;
  adaptability: number;
  mathematical_accuracy: number;
}

export interface SessionEndResponse {
  scores: Scores;
  feedback: string;
  session_summary: string;
}

export const PERSONAS: PersonaInfo[] = [
  {
    name: 'Struggling Sam',
    type: 'struggling_sam',
    description: 'Struggles with basic concepts, needs patience and step-by-step guidance'
  },
  {
    name: 'Overconfident Olivia',
    type: 'overconfident_olivia',
    description: 'Rushes to conclusions, resists correction, needs careful guidance'
  },
  {
    name: 'Anxious Alex',
    type: 'anxious_alex',
    description: 'Knows the material but lacks confidence, needs encouragement'
  },
  {
    name: 'Methodical Maya',
    type: 'methodical_maya',
    description: 'Asks deep questions, wants to understand the "why" behind concepts'
  }
];