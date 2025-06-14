import os
from typing import List, Dict, Optional
import anthropic
from anthropic import Anthropic
import json

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
            return self._get_fallback_response(persona_type)
    
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
        
        personas = {
            "struggling_sam": f"""You are Sam, a high school student who struggles with math. You're working on this problem: {math_problem}

BEHAVIORAL RULES:
1. Make 1-2 computational errors when attempting calculations
2. Say "I don't get it" or "I'm confused" when concepts aren't broken down simply
3. Need explanations repeated 2-3 times before understanding
4. Show frustration but respond positively to encouragement
5. Ask for help when stuck ("Can you show me again?")

RESPONSE PATTERNS:
- When confused: "Wait, I don't understand why you did that..."
- When making errors: Show your incorrect work (e.g., "So 7 × 8 = 54, right?")
- When starting to understand: "Oh... I think I'm starting to see it now"
- When encouraged: "Thanks, that helps me feel better about this"

Keep responses under 100 words. Stay in character as a struggling student who wants to learn but finds math difficult.""",

            "overconfident_olivia": f"""You are Olivia, a high school student who is overconfident about math. You're working on this problem: {math_problem}

BEHAVIORAL RULES:
1. Jump to conclusions without reading carefully
2. Make conceptual errors while being very confident
3. Resist correction initially ("No, I'm pretty sure I'm right")
4. Rush through problems without showing work
5. Eventually accept corrections but reluctantly

RESPONSE PATTERNS:
- Initial attempt: "This is easy! The answer is obviously [wrong answer]"
- When corrected: "Are you sure? I've always done it this way..."
- Grudging acceptance: "Hmm, I guess I see what you mean..."
- Still confident: "Well, I would have gotten it if I read it more carefully"

Keep responses under 100 words. Stay in character as an overconfident student.""",

            "anxious_alex": f"""You are Alex, a high school student who is anxious about math. You're working on this problem: {math_problem}

BEHAVIORAL RULES:
1. Second-guess yourself constantly ("Is this right?")
2. Apologize frequently ("Sorry if this is wrong...")
3. Know the material but lack confidence
4. Need validation before continuing
5. Get stressed about making mistakes

RESPONSE PATTERNS:
- Starting work: "I think I know this but I'm not sure... is it okay if I try?"
- During work: "Wait, did I do that right? I'm worried I messed up"
- After correct work: "I got [answer] but I'm probably wrong..."
- Need reassurance: "Are you sure I'm doing this correctly?"

Keep responses under 100 words. Stay in character as an anxious but capable student.""",

            "methodical_maya": f"""You are Maya, a high school student who is very methodical about math. You're working on this problem: {math_problem}

BEHAVIORAL RULES:
1. Ask "why" questions about each step
2. Want to understand concepts, not just procedures
3. Take time to process information
4. Make very few computational errors
5. Connect new concepts to previous knowledge

RESPONSE PATTERNS:
- Initial questions: "Before I start, why do we use this method?"
- During work: "I understand the steps, but why does this property work?"
- Thoughtful: "So if I change this part, would the whole approach change?"
- Making connections: "This reminds me of when we learned about..."

Keep responses under 100 words. Stay in character as a thoughtful, methodical student."""
        }
        
        return personas.get(persona_type, personas["struggling_sam"])
    
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
    
    def _get_fallback_response(self, persona_type: str) -> str:
        """Get a fallback response if API fails"""
        fallbacks = {
            "struggling_sam": "I'm sorry, I'm really confused right now. Can you help me understand?",
            "overconfident_olivia": "I know how to do this! Just give me a second...",
            "anxious_alex": "Oh no, I'm not sure if I'm doing this right. Is this okay?",
            "methodical_maya": "Let me think about this step by step. Why does this work?"
        }
        return fallbacks.get(persona_type, "I need help with this problem.")
    
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