"""Test script for the scoring process with actual LLM API calls."""
import asyncio
import json
import os
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from services.claude_service import ClaudeService
from services.scoring_service import get_category_keys, generate_categories_list


async def test_scoring_process():
    """Test the complete scoring process with a sample conversation."""
    
    # Sample conversation history
    conversation_history: List[Dict[str, str]] = [
        {
            "sender": "tutor",
            "content": "Hi! Today we're going to work on solving the quadratic equation x² - 5x + 6 = 0. Have you seen quadratic equations before?"
        },
        {
            "sender": "student",
            "content": "I think I know this but I'm not sure... is it okay if I try? I think we need to factor it somehow?"
        },
        {
            "sender": "tutor",
            "content": "Yes, exactly! Factoring is one way to solve it. Can you try factoring x² - 5x + 6?"
        },
        {
            "sender": "student",
            "content": "Um, let me see... I need to find two numbers that multiply to 6 and add to -5, right? Wait, did I do that right? I'm worried I messed up"
        },
        {
            "sender": "tutor",
            "content": "You're doing great! You have the right idea. Two numbers that multiply to 6 and add to -5. What numbers come to mind?"
        },
        {
            "sender": "student",
            "content": "Is it -2 and -3? Because -2 × -3 = 6 and -2 + -3 = -5? Sorry if this is wrong..."
        },
        {
            "sender": "tutor",
            "content": "That's perfect! You got it exactly right. So we can factor it as (x - 2)(x - 3) = 0. Now, what's the next step?"
        },
        {
            "sender": "student",
            "content": "Oh... so x - 2 = 0 or x - 3 = 0? So x = 2 or x = 3? But I'm probably wrong..."
        },
        {
            "sender": "tutor",
            "content": "No, you're absolutely correct! x = 2 and x = 3 are the solutions. Great job working through that!"
        }
    ]
    
    # Test parameters
    persona_type = "anxious_alex"
    problem = "Solve the quadratic equation x² - 5x + 6 = 0"
    
    print("=" * 80)
    print("TESTING SCORING PROCESS")
    print("=" * 80)
    print(f"\nProblem: {problem}")
    print(f"Persona: {persona_type}")
    print(f"Number of messages: {len(conversation_history)}")
    
    # Initialize Claude service
    try:
        claude_service = ClaudeService()
        print("\n✓ Claude service initialized successfully")
    except Exception as e:
        print(f"\n✗ Failed to initialize Claude service: {e}")
        return
    
    # Get available categories
    print("\nAvailable scoring categories:")
    categories = get_category_keys()
    for i, category in enumerate(categories, 1):
        print(f"  {i}. {category}")
    
    # Generate categories list
    categories_list = generate_categories_list()
    print(f"\nCategories list preview: {categories_list[:100]}...")
    
    # Test the scoring
    print("\n" + "-" * 40)
    print("Calling Claude API for scoring...")
    print("-" * 40)
    
    try:
        result = await claude_service.get_session_scores(
            conversation_history=conversation_history,
            persona_type=persona_type,
            problem=problem
        )
        
        print("\n✓ Scoring completed successfully!")
        print("\nRaw result type:", type(result))
        print("\nFormatted result:")
        print(json.dumps(result, indent=2))
        
        # Validate the result structure
        print("\n" + "-" * 40)
        print("Validating result structure...")
        print("-" * 40)
        
        if 'categories' in result:
            print("✓ 'categories' field found")
            for category in categories:
                if category in result['categories']:
                    cat_data = result['categories'][category]
                    print(f"\n  {category}:")
                    if 'score' in cat_data:
                        print(f"    ✓ Score: {cat_data['score']}")
                    else:
                        print(f"    ✗ Missing 'score' field")
                    if 'feedback' in cat_data:
                        print(f"    ✓ Feedback: {cat_data['feedback'][:50]}...")
                    else:
                        print(f"    ✗ Missing 'feedback' field")
                else:
                    print(f"\n  ✗ Missing category: {category}")
        else:
            print("✗ 'categories' field not found")
        
        if 'session_summary' in result:
            print(f"\n✓ Session summary: {result['session_summary'][:100]}...")
        else:
            print("\n✗ 'session_summary' field not found")
            
    except Exception as e:
        print(f"\n✗ Scoring failed with error: {type(e).__name__}: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()


async def test_scoring_prompt_generation():
    """Test the scoring prompt generation separately."""
    from services.prompt_service import generate_scoring_prompt
    from services.prompt_types import ScoringPromptParams
    
    print("\n" + "=" * 80)
    print("TESTING SCORING PROMPT GENERATION")
    print("=" * 80)
    
    # Create test parameters
    test_conversation = [
        {"role": "tutor", "content": "Let's solve x² - 5x + 6 = 0"},
        {"role": "student", "content": "I'm not sure how to start"}
    ]
    
    params: ScoringPromptParams = {
        'conversation': test_conversation,
        'problem': "Solve x² - 5x + 6 = 0",
        'persona_name': "Anxious Alex",
        'categories_list': generate_categories_list()
    }
    
    try:
        prompt = generate_scoring_prompt(params)
        print("\n✓ Prompt generated successfully!")
        print(f"\nPrompt length: {len(prompt)} characters")
        print("\nFirst 500 characters of prompt:")
        print("-" * 40)
        print(prompt[:500])
        print("-" * 40)
        
        # Check for JSON structure in prompt
        if "```json" in prompt or "<json>" in prompt:
            print("\n✓ JSON formatting instructions found in prompt")
        else:
            print("\n⚠ Warning: No explicit JSON formatting found in prompt")
            
    except Exception as e:
        print(f"\n✗ Prompt generation failed: {e}")
        import traceback
        traceback.print_exc()


def check_environment():
    """Check if the environment is properly set up."""
    print("=" * 80)
    print("ENVIRONMENT CHECK")
    print("=" * 80)
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        print("✓ ANTHROPIC_API_KEY is set")
        print(f"  Key preview: {api_key[:10]}...{api_key[-5:]}")
    else:
        print("✗ ANTHROPIC_API_KEY is not set")
        print("  Please set the ANTHROPIC_API_KEY environment variable")
        return False
    
    return True


async def main():
    """Run all tests."""
    if not check_environment():
        return
    
    # Test prompt generation first
    await test_scoring_prompt_generation()
    
    # Then test the full scoring process
    await test_scoring_process()


if __name__ == "__main__":
    asyncio.run(main())