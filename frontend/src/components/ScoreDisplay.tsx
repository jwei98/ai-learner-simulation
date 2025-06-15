import React, { useEffect, useState } from 'react';
import type { SessionEndResponse } from '../types';
import { sessionApi, type ScoringCategory } from '../services/api';

interface ScoreDisplayProps {
  scores: SessionEndResponse;
  onNewSession: () => void;
}

export const ScoreDisplay: React.FC<ScoreDisplayProps> = ({ scores, onNewSession }) => {
  const [scoreCategories, setScoreCategories] = useState<ScoringCategory[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const categories = await sessionApi.getScoringCategories();
        setScoreCategories(categories);
      } catch (error) {
        console.error('Failed to fetch scoring categories:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

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
        {loading ? (
          <div className="text-center text-gray-500">Loading categories...</div>
        ) : (
          <div className="space-y-4">
            {scoreCategories.map(({ key, label }) => {
              const category = scores.categories[key];
              if (!category) return null;
              
              return (
                <div key={key} className="mb-4">
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium">{label}</span>
                    <span className={`text-sm font-bold ${getScoreColor(category.score)}`}>
                      {category.score}/5
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                      style={{ width: getScoreBarWidth(category.score) }}
                    />
                  </div>
                  <p className="text-sm text-gray-600 italic">{category.feedback}</p>
                </div>
              );
            })}
          </div>
        )}
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