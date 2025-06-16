import os
from typing import List, Dict, Optional
import anthropic
from anthropic import Anthropic
import json
from .persona_service import load_persona_prompt
from .prompt_service import generate_scoring_prompt
from .prompt_types import ScoringPromptParams, ConversationMessage
from .scoring_service import get_category_keys, generate_categories_list

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
        
        response = self.client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=300,
            temperature=0.7,
            system=system_prompt,
            messages=claude_messages
        )
        
        return response.content[0].text
    
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

        print(scoring_prompt)
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            temperature=0,
            messages=[{
                "role": "user",
                "content": scoring_prompt
            }]
        )

        print(response)
        
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
                for key in get_category_keys():
                    score = old_scores.get(key)
                    if score is None:
                        raise ValueError(f"Missing score for category: {key}")
                    
                    if isinstance(old_feedback, dict):
                        feedback = old_feedback.get(key)
                        if feedback is None:
                            raise ValueError(f"Missing feedback for category: {key}")
                    else:
                        feedback = old_feedback if isinstance(old_feedback, str) else None
                        if feedback is None:
                            raise ValueError(f"Invalid feedback format")
                    
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
    
    def _get_persona_prompt(self, persona_type: str, problem: str) -> str:
        """Get the system prompt for a specific persona"""
        
        # Use the shared persona service to load the prompt
        persona_prompt = load_persona_prompt(persona_type, problem)
        
        if not persona_prompt:
            raise ValueError(f"Failed to load persona prompt for: {persona_type}")
        return persona_prompt
    
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
        
        # Format conversation as list of messages
        conversation: List[ConversationMessage] = [
            {
                'role': msg['sender'],
                'content': msg['content']
            }
            for msg in conversation_history
        ]
        
        # Convert persona type to display name
        persona_name = persona_type.replace('_', ' ').title()
        
        # Generate categories list
        categories_list = generate_categories_list()
        
        # Create typed parameters for scoring prompt
        params: ScoringPromptParams = {
            'conversation': conversation,
            'problem': problem,
            'persona_name': persona_name,
            'categories_list': categories_list
        }
        
        # Generate the scoring prompt with typed parameters
        return generate_scoring_prompt(params)

# Create a singleton instance (will be initialized on first use)
_claude_service = None

def get_claude_service():
    global _claude_service
    if _claude_service is None:
        _claude_service = ClaudeService()
    return _claude_service

claude_service = get_claude_service()