import React, { useState, useEffect, useRef } from 'react';
import { MessageBubble } from './MessageBubble';
import { MessageInput } from './MessageInput';
import { sessionApi } from '../services/api';
import type { Message, SessionEndResponse } from '../types';

interface ChatInterfaceProps {
  sessionId: string;
  initialMessage: string;
  personaName: string;
  problem: string;
  onEnd: (scores: SessionEndResponse) => void;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  sessionId,
  initialMessage,
  personaName,
  problem,
  onEnd
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionActive, setSessionActive] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Add initial AI message
    const initialAiMessage: Message = {
      id: '1',
      content: initialMessage,
      sender: 'learner',
      timestamp: new Date().toISOString()
    };
    setMessages([initialAiMessage]);
  }, [initialMessage]);

  useEffect(() => {
    // Scroll to bottom when messages change
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (content: string) => {
    if (!sessionActive || isLoading) return;

    // Add tutor message
    const tutorMessage: Message = {
      id: `${messages.length + 1}`,
      content,
      sender: 'tutor',
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, tutorMessage]);

    setIsLoading(true);
    try {
      const response = await sessionApi.sendMessage(sessionId, {
        message: content,
        sender: 'tutor'
      });

      // Add AI response
      const aiMessage: Message = {
        id: `${messages.length + 2}`,
        content: response.response,
        sender: 'learner',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, aiMessage]);
      setSessionActive(response.session_active);
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message
      const errorMessage: Message = {
        id: `${messages.length + 2}`,
        content: 'Sorry, I had trouble understanding that. Can you try again?',
        sender: 'learner',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEndSession = async () => {
    if (!sessionActive) return;

    setIsLoading(true);
    try {
      const scores = await sessionApi.endSession(sessionId);
      onEnd(scores);
    } catch (error) {
      console.error('Error ending session:', error);
      alert('Failed to end session. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-h-screen">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-xl font-semibold">Tutoring Session with {personaName}</h2>
            <p className="text-sm text-gray-600 mt-1">Problem: {problem}</p>
          </div>
          <button
            onClick={handleEndSession}
            disabled={isLoading || !sessionActive}
            className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            End Session
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto bg-gray-50 p-4">
        <div className="max-w-4xl mx-auto">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          {isLoading && (
            <div className="flex justify-start mb-4">
              <div className="bg-gray-200 rounded-lg px-4 py-2">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <MessageInput 
        onSend={sendMessage} 
        disabled={isLoading || !sessionActive} 
      />
    </div>
  );
};