import React, { useState, useEffect } from 'react';
import { Persona, PersonaType } from '../types';
import { sessionApi } from '../services/api';

interface SessionSetupProps {
  onStart: (tutorName: string, problem: string, personaType: PersonaType) => void;
  isLoading?: boolean;
}

export const SessionSetup: React.FC<SessionSetupProps> = ({ onStart, isLoading }) => {
  const [tutorName, setTutorName] = useState('');
  const [problem, setProblem] = useState('');
  const [personaType, setPersonaType] = useState<PersonaType>('');
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [loadingPersonas, setLoadingPersonas] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPersonas = async () => {
      try {
        const fetchedPersonas = await sessionApi.getPersonas();
        setPersonas(fetchedPersonas);
        // Set default persona to the first one
        if (fetchedPersonas.length > 0) {
          setPersonaType(fetchedPersonas[0].id);
        }
      } catch (error) {
        console.error('Failed to fetch personas:', error);
        setError('Failed to load personas. Please refresh the page.');
      } finally {
        setLoadingPersonas(false);
      }
    };

    fetchPersonas();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (tutorName.trim() && problem.trim()) {
      onStart(tutorName.trim(), problem.trim(), personaType);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Start a New Tutoring Session</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="tutorName" className="block text-sm font-medium text-gray-700 mb-2">
            Your Name
          </label>
          <input
            id="tutorName"
            type="text"
            value={tutorName}
            onChange={(e) => setTutorName(e.target.value)}
            placeholder="Enter your name"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div>
          <label htmlFor="problem" className="block text-sm font-medium text-gray-700 mb-2">
            Problem
          </label>
          <textarea
            id="problem"
            value={problem}
            onChange={(e) => setProblem(e.target.value)}
            placeholder="Enter the problem (e.g., 'Solve for x: 2x + 5 = 13')"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Student Persona
          </label>
          {loadingPersonas ? (
            <div className="text-gray-500">Loading personas...</div>
          ) : error ? (
            <div className="text-red-500">{error}</div>
          ) : personas.length === 0 ? (
            <div className="text-gray-500">No personas available</div>
          ) : (
            <div className="space-y-2">
              {personas.map((persona) => (
                <label
                  key={persona.id}
                  className="flex items-start p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50"
                >
                  <input
                    type="radio"
                    name="persona"
                    value={persona.id}
                    checked={personaType === persona.id}
                    onChange={(e) => setPersonaType(e.target.value)}
                    className="mt-1 mr-3"
                  />
                  <div>
                    <div className="font-medium">{persona.name}</div>
                  </div>
                </label>
              ))}
            </div>
          )}
        </div>

        <button
          type="submit"
          disabled={isLoading || !tutorName.trim() || !problem.trim() || personas.length === 0}
          className="w-full py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? 'Starting Session...' : 'Start Session'}
        </button>
      </form>
    </div>
  );
};