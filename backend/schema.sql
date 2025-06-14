-- PostgreSQL schema for AI Tutor Training Platform

-- Sessions table
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tutor_name VARCHAR(255) NOT NULL,
    persona_type VARCHAR(50) NOT NULL,
    math_problem TEXT NOT NULL,
    conversation_history JSONB NOT NULL DEFAULT '[]',
    scores JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true
);

-- Indexes for performance
CREATE INDEX idx_sessions_tutor_name ON sessions(tutor_name);
CREATE INDEX idx_sessions_created_at ON sessions(created_at);
CREATE INDEX idx_sessions_persona_type ON sessions(persona_type);

-- Tutor profiles table (for progress tracking)
CREATE TABLE IF NOT EXISTS tutor_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    total_sessions INTEGER DEFAULT 0,
    average_scores JSONB,
    last_session_at TIMESTAMP WITH TIME ZONE
);

-- Messages table (optional, for detailed message tracking)
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    sender VARCHAR(20) NOT NULL CHECK (sender IN ('tutor', 'learner')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_session_id ON messages(session_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);