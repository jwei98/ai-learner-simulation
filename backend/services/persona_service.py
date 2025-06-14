from typing import List, Optional
from .prompt_service import load_prompt, list_prompts_in_directory

def get_available_personas() -> List[str]:
    """Get list of available personas from the personas directory"""
    return list_prompts_in_directory("personas")

def load_persona_prompt(persona_type: str, math_problem: str) -> Optional[str]:
    """Load a persona prompt from file and replace placeholders"""
    # Try to load the specific persona
    persona_prompt = load_prompt(f"personas/{persona_type}.md", math_problem=math_problem)
    
    # If that fails, try to load any available persona as fallback
    if not persona_prompt:
        available_personas = get_available_personas()
        if available_personas:
            fallback_persona = available_personas[0]
            print(f"Warning: Persona '{persona_type}' not found. Using '{fallback_persona}' as fallback.")
            persona_prompt = load_prompt(f"personas/{fallback_persona}.md", math_problem=math_problem)
    
    return persona_prompt