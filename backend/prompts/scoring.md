Analyze this tutoring conversation and score the tutor on 5 dimensions (1-5 scale).

CONTEXT:
- Math Problem: {math_problem}
- Student Persona: {persona_name}
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
{
  "scores": {
    "explanation_clarity": <1-5>,
    "patience_encouragement": <1-5>,
    "active_questioning": <1-5>,
    "adaptability": <1-5>,
    "mathematical_accuracy": <1-5>
  },
  "feedback": "<2-3 sentences of specific, actionable feedback>",
  "session_summary": "<1-2 sentences summarizing the session>"
}