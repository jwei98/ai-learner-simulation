import os
from typing import List, Dict, Optional
import anthropic
from anthropic import Anthropic
import json
from .persona_service import load_persona_prompt
from .prompt_service import load_prompt

class ClaudeService:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        
        self.client = Anthropic(api_key=api_key)
        
    async def get_persona_response(
        self, 
        messages: List[Dict[str, str]], 
        persona_type: str,
        problem: str
    ) -> str:
        """Get a response from Claude Haiku based on the persona type"""
        
        # Get the persona prompt
        system_prompt = self._get_persona_prompt(persona_type, problem)
        
        # Format messages for Claude API
        claude_messages = self._format_messages_for_claude(messages)
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-haiku-latest",
                max_tokens=300,
                temperature=0.7,
                system=system_prompt,
                messages=claude_messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            # Fallback response
            return "I need help with this problem."
    
    async def get_session_scores(
        self,
        conversation_history: List[Dict[str, str]],
        persona_type: str,
        problem: str
    ) -> Dict:
        """Get scoring from Claude Sonnet for the tutoring session"""
        
        scoring_prompt = self._get_scoring_prompt(
            conversation_history, 
            persona_type, 
            problem
        )
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                temperature=0,
                messages=[{
                    "role": "user",
                    "content": scoring_prompt
                }]
            )
            
            # Parse JSON response
            response_text = response.content[0].text
            # Extract JSON from response (it might be wrapped in text)
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                
                # Handle old format - convert to new nested structure
                if 'scores' in result and 'feedback' in result:
                    old_scores = result.get('scores', {})
                    old_feedback = result.get('feedback', {})
                    
                    # Convert to new format
                    categories = {}
                    for key in ['explanation_clarity', 'patience_encouragement', 'active_questioning', 'adaptability', 'mathematical_accuracy']:
                        score = old_scores.get(key, 3)
                        if isinstance(old_feedback, dict):
                            feedback = old_feedback.get(key, "No specific feedback available.")
                        else:
                            feedback = old_feedback if isinstance(old_feedback, str) else "No specific feedback available."
                        
                        categories[key] = {
                            'score': score,
                            'feedback': feedback
                        }
                    
                    result = {
                        'categories': categories,
                        'session_summary': result.get('session_summary', 'Session completed.')
                    }
                
                return result
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as e:
            print(f"Error getting scores: {e}")
            # Return default scores
            return {
                "categories": {
                    "explanation_clarity": {
                        "score": 3,
                        "feedback": "Unable to evaluate explanation clarity."
                    },
                    "patience_encouragement": {
                        "score": 3,
                        "feedback": "Unable to evaluate patience and encouragement."
                    },
                    "active_questioning": {
                        "score": 3,
                        "feedback": "Unable to evaluate active questioning."
                    },
                    "adaptability": {
                        "score": 3,
                        "feedback": "Unable to evaluate adaptability."
                    },
                    "mathematical_accuracy": {
                        "score": 3,
                        "feedback": "Unable to evaluate mathematical accuracy."
                    }
                },
                "session_summary": "Session completed. Unable to generate detailed analysis."
            }
    
    def _get_persona_prompt(self, persona_type: str, problem: str) -> str:
        """Get the system prompt for a specific persona"""
        
        # Use the shared persona service to load the prompt
        persona_prompt = load_persona_prompt(persona_type, problem)
        print(persona_prompt)
        
        if persona_prompt:
            return persona_prompt
        else:
            # Fallback if persona loading fails
            return f"You are a high school student working on this problem: {problem}. Respond as the {persona_type.replace('_', ' ')} student."
    
    def _format_messages_for_claude(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Format message history for Claude API"""
        claude_messages = []
        
        for msg in messages:
            role = "user" if msg["sender"] == "tutor" else "assistant"
            claude_messages.append({
                "role": role,
                "content": msg["content"]
            })
        
        # Ensure we start with a user message
        if not claude_messages or claude_messages[0]["role"] != "user":
            claude_messages.insert(0, {
                "role": "user",
                "content": "Let's work on this math problem together."
            })
        
        # Ensure we end with a user message (for the next response)
        if claude_messages[-1]["role"] != "user":
            claude_messages.append({
                "role": "user",
                "content": "Please continue."
            })
        
        return claude_messages
    
    def _get_scoring_prompt(
        self, 
        conversation_history: List[Dict[str, str]], 
        persona_type: str,
        problem: str
    ) -> str:
        """Generate the scoring prompt for Claude Sonnet"""
        
        # Format conversation
        conversation = "\n".join([
            f"{msg['sender'].upper()}: {msg['content']}"
            for msg in conversation_history
        ])
        
        # Convert persona type to display name
        persona_name = persona_type.replace('_', ' ').title()
        
        # Load the scoring prompt template
        scoring_prompt = load_prompt(
            "scoring.md",
            problem=problem,
            persona_name=persona_name,
            conversation=conversation
        )
        
        # Fallback if prompt loading fails
        if not scoring_prompt:
            return f"""Analyze this tutoring conversation and score the tutor on 5 dimensions (1-5 scale).

CONTEXT:
- Problem: {problem}
- Student Persona: {persona_name}
- Conversation:

{conversation}

Return your analysis in JSON format with scores for: explanation_clarity, patience_encouragement, active_questioning, adaptability, mathematical_accuracy (all 1-5), plus feedback and session_summary fields."""
        
        return scoring_prompt

# Create a singleton instance (will be initialized on first use)
_claude_service = None

def get_claude_service():
    global _claude_service
    if _claude_service is None:
        _claude_service = ClaudeService()
    return _claude_service

claude_service = get_claude_service()