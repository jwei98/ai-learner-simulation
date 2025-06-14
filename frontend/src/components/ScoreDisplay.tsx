import React from 'react';
import type { SessionEndResponse } from '../types';

interface ScoreDisplayProps {
  scores: SessionEndResponse;
  onNewSession: () => void;
}

export const ScoreDisplay: React.FC<ScoreDisplayProps> = ({ scores, onNewSession }) => {
  const scoreCategories = [
    { key: 'explanation_clarity', label: 'Explanation Clarity' },
    { key: 'patience_encouragement', label: 'Patience & Encouragement' },
    { key: 'active_questioning', label: 'Active Questioning' },
    { key: 'adaptability', label: 'Adaptability' },
    { key: 'mathematical_accuracy', label: 'Mathematical Accuracy' }
  ];

  const getScoreColor = (score: number) => {
    if (score >= 4) return 'text-green-600';
    if (score >= 3) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBarWidth = (score: number) => `${(score / 5) * 100}%`;

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Session Results</h2>

      {/* Score Summary */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold mb-4">Performance Scores</h3>
        <div className="space-y-4">
          {scoreCategories.map(({ key, label }) => {
            const score = scores.scores[key as keyof typeof scores.scores];
            return (
              <div key={key}>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium">{label}</span>
                  <span className={`text-sm font-bold ${getScoreColor(score)}`}>
                    {score}/5
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: getScoreBarWidth(score) }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Feedback */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold mb-2">Feedback</h3>
        <p className="text-gray-700">{scores.feedback}</p>
      </div>

      {/* Session Summary */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold mb-2">Session Summary</h3>
        <p className="text-gray-700">{scores.session_summary}</p>
      </div>

      {/* Action Button */}
      <button
        onClick={onNewSession}
        className="w-full py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
      >
        Start New Session
      </button>
    </div>
  );
};