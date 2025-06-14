import os
from typing import List, Dict, Optional
import anthropic
from anthropic import Anthropic
import json
from .persona_service import load_persona_prompt

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
        math_problem: str
    ) -> str:
        """Get a response from Claude Haiku based on the persona type"""
        
        # Get the persona prompt
        system_prompt = self._get_persona_prompt(persona_type, math_problem)
        
        # Format messages for Claude API
        claude_messages = self._format_messages_for_claude(messages)
        
        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
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
        math_problem: str
    ) -> Dict:
        """Get scoring from Claude Sonnet for the tutoring session"""
        
        scoring_prompt = self._get_scoring_prompt(
            conversation_history, 
            persona_type, 
            math_problem
        )
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
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
                return json.loads(json_match.group())
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as e:
            print(f"Error getting scores: {e}")
            # Return default scores
            return {
                "scores": {
                    "explanation_clarity": 3,
                    "patience_encouragement": 3,
                    "active_questioning": 3,
                    "adaptability": 3,
                    "mathematical_accuracy": 3
                },
                "feedback": "Unable to generate detailed feedback at this time.",
                "session_summary": "Session completed."
            }
    
    def _get_persona_prompt(self, persona_type: str, math_problem: str) -> str:
        """Get the system prompt for a specific persona"""
        
        # Use the shared persona service to load the prompt
        persona_prompt = load_persona_prompt(persona_type, math_problem)
        
        if persona_prompt:
            return persona_prompt
        else:
            # Fallback if persona loading fails
            return f"You are a high school student working on this problem: {math_problem}. Respond as the {persona_type.replace('_', ' ')} student."
    
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
        math_problem: str
    ) -> str:
        """Generate the scoring prompt for Claude Sonnet"""
        
        # Format conversation
        conversation = "\n".join([
            f"{msg['sender'].upper()}: {msg['content']}"
            for msg in conversation_history
        ])
        
        return f"""Analyze this tutoring conversation and score the tutor on 5 dimensions (1-5 scale).

CONTEXT:
- Math Problem: {math_problem}
- Student Persona: {persona_type.replace('_', ' ').title()}
- Conversation:

{conversation}

SCORING RUBRIC:
1. Explanation Clarity (1-5):
   - 5: Breaks down complex concepts clearly, logical progression
   - 3: Adequate explanations with some gaps
   - 1: Confusing explanations, skips steps

2. Patience & Encouragement (1-5):
   - 5: Consistently supportive, handles frustration well
   - 3: Generally patient with occasional lapses
   - 1: Shows impatience or discouraging responses

3. Active Questioning (1-5):
   - 5: Asks probing questions to check understanding
   - 3: Some follow-up questions
   - 1: Rarely checks for understanding

4. Adaptability (1-5):
   - 5: Adjusts approach based on learner responses
   - 3: Makes some adjustments when prompted
   - 1: Same approach regardless of feedback

5. Mathematical Accuracy (1-5):
   - 5: All content mathematically correct
   - 3: Mostly accurate with minor errors
   - 1: Significant mathematical errors

Return your analysis in this exact JSON format:
{{
  "scores": {{
    "explanation_clarity": <1-5>,
    "patience_encouragement": <1-5>,
    "active_questioning": <1-5>,
    "adaptability": <1-5>,
    "mathematical_accuracy": <1-5>
  }},
  "feedback": "<2-3 sentences of specific, actionable feedback>",
  "session_summary": "<1-2 sentences summarizing the session>"
}}"""

# Create a singleton instance (will be initialized on first use)
_claude_service = None

def get_claude_service():
    global _claude_service
    if _claude_service is None:
        _claude_service = ClaudeService()
    return _claude_service

claude_service = get_claude_service()