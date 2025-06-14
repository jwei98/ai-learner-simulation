import React, { useState } from 'react';
import { PERSONAS, PersonaType } from '../types';

interface SessionSetupProps {
  onStart: (tutorName: string, mathProblem: string, personaType: PersonaType) => void;
  isLoading?: boolean;
}

export const SessionSetup: React.FC<SessionSetupProps> = ({ onStart, isLoading }) => {
  const [tutorName, setTutorName] = useState('');
  const [mathProblem, setMathProblem] = useState('');
  const [personaType, setPersonaType] = useState<PersonaType>('struggling_sam');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (tutorName.trim() && mathProblem.trim()) {
      onStart(tutorName.trim(), mathProblem.trim(), personaType);
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
          <label htmlFor="mathProblem" className="block text-sm font-medium text-gray-700 mb-2">
            Math Problem
          </label>
          <textarea
            id="mathProblem"
            value={mathProblem}
            onChange={(e) => setMathProblem(e.target.value)}
            placeholder="Enter the math problem (e.g., 'Solve for x: 2x + 5 = 13')"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Student Persona
          </label>
          <div className="space-y-2">
            {PERSONAS.map((persona) => (
              <label
                key={persona.type}
                className="flex items-start p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50"
              >
                <input
                  type="radio"
                  name="persona"
                  value={persona.type}
                  checked={personaType === persona.type}
                  onChange={(e) => setPersonaType(e.target.value as PersonaType)}
                  className="mt-1 mr-3"
                />
                <div>
                  <div className="font-medium">{persona.name}</div>
                  <div className="text-sm text-gray-600">{persona.description}</div>
                </div>
              </label>
            ))}
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading || !tutorName.trim() || !mathProblem.trim()}
          className="w-full py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? 'Starting Session...' : 'Start Session'}
        </button>
      </form>
    </div>
  );
};