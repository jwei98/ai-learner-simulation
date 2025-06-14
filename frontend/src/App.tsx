import { useState } from 'react';
import { SessionSetup } from './components/SessionSetup';
import { ChatInterface } from './components/ChatInterface';
import { ScoreDisplay } from './components/ScoreDisplay';
import { sessionApi } from './services/api';
import type { PersonaType, SessionEndResponse } from './types';

type AppState = 
  | { type: 'setup' }
  | { type: 'loading' }
  | { type: 'chat'; sessionId: string; initialMessage: string; personaName: string; problem: string }
  | { type: 'scores'; scores: SessionEndResponse };

function App() {
  const [state, setState] = useState<AppState>({ type: 'setup' });

  const handleStartSession = async (
    tutorName: string, 
    problem: string, 
    personaType: PersonaType
  ) => {
    setState({ type: 'loading' });
    
    try {
      const response = await sessionApi.startSession({
        tutor_name: tutorName,
        problem: problem,
        persona_type: personaType
      });

      setState({
        type: 'chat',
        sessionId: response.session_id,
        initialMessage: response.initial_response,
        personaName: response.persona_info.name,
        problem: problem
      });
    } catch (error) {
      console.error('Error starting session:', error);
      alert('Failed to start session. Please check your connection and try again.');
      setState({ type: 'setup' });
    }
  };

  const handleEndSession = (scores: SessionEndResponse) => {
    setState({ type: 'scores', scores });
  };

  const handleNewSession = () => {
    setState({ type: 'setup' });
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {state.type === 'setup' && (
        <div className="container mx-auto py-8">
          <h1 className="text-3xl font-bold text-center mb-8">
            AI Tutor Training Platform
          </h1>
          <SessionSetup onStart={handleStartSession} />
        </div>
      )}

      {state.type === 'loading' && (
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-600">Starting session...</p>
          </div>
        </div>
      )}

      {state.type === 'chat' && (
        <ChatInterface
          sessionId={state.sessionId}
          initialMessage={state.initialMessage}
          personaName={state.personaName}
          problem={state.problem}
          onEnd={handleEndSession}
        />
      )}

      {state.type === 'scores' && (
        <div className="container mx-auto py-8">
          <h1 className="text-3xl font-bold text-center mb-8">
            AI Tutor Training Platform
          </h1>
          <ScoreDisplay 
            scores={state.scores} 
            onNewSession={handleNewSession} 
          />
        </div>
      )}
    </div>
  );
}

export default App;