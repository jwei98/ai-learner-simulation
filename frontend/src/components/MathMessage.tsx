import React from 'react';
import 'katex/dist/katex.min.css';
import { InlineMath, BlockMath } from 'react-katex';

interface MathMessageProps {
  content: string;
}

export const MathMessage: React.FC<MathMessageProps> = ({ content }) => {
  // Split content by display math delimiters ($$...$$)
  const displayMathRegex = /\$\$(.*?)\$\$/gs;
  const parts: (string | { type: 'display'; math: string })[] = [];
  let lastIndex = 0;

  content.replace(displayMathRegex, (match, math, index) => {
    // Add text before the match
    if (index > lastIndex) {
      parts.push(content.slice(lastIndex, index));
    }
    // Add the display math
    parts.push({ type: 'display', math });
    lastIndex = index + match.length;
    return match;
  });

  // Add remaining text
  if (lastIndex < content.length) {
    parts.push(content.slice(lastIndex));
  }

  // Process each part for inline math
  const processInlineMath = (text: string) => {
    const inlineMathRegex = /\$(.*?)\$/g;
    const inlineParts: (string | { type: 'inline'; math: string })[] = [];
    let inlineLastIndex = 0;

    text.replace(inlineMathRegex, (match, math, index) => {
      // Add text before the match
      if (index > inlineLastIndex) {
        inlineParts.push(text.slice(inlineLastIndex, index));
      }
      // Add the inline math
      inlineParts.push({ type: 'inline', math });
      inlineLastIndex = index + match.length;
      return match;
    });

    // Add remaining text
    if (inlineLastIndex < text.length) {
      inlineParts.push(text.slice(inlineLastIndex));
    }

    return inlineParts.map((part, idx) => {
      if (typeof part === 'string') {
        return <span key={idx}>{part}</span>;
      } else {
        return <InlineMath key={idx} math={part.math} />;
      }
    });
  };

  return (
    <>
      {parts.map((part, index) => {
        if (typeof part === 'string') {
          return <span key={index}>{processInlineMath(part)}</span>;
        } else if (part.type === 'display') {
          return (
            <div key={index} className="my-2">
              <BlockMath math={part.math} />
            </div>
          );
        }
        return null;
      })}
    </>
  );
};