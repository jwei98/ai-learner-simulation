import React from 'react';
import type { Message } from '../types';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isTutor = message.sender === 'tutor';
  
  return (
    <div className={`flex ${isTutor ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`
          max-w-[70%] rounded-lg px-4 py-2 
          ${isTutor 
            ? 'bg-blue-500 text-white' 
            : 'bg-gray-200 text-gray-800'
          }
        `}
      >
        <div className="text-sm font-semibold mb-1">
          {isTutor ? 'You (Tutor)' : 'Student'}
        </div>
        <div className="whitespace-pre-wrap">{message.content}</div>
        <div className="text-xs opacity-70 mt-1">
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};