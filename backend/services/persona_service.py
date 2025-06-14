from typing import List, Optional
from .prompt_service import load_prompt, list_prompts_in_directory

def get_available_personas() -> List[str]:
    """Get list of available personas from the personas directory"""
    return list_prompts_in_directory("personas")

def load_persona_prompt(persona_type: str, problem: str) -> Optional[str]:
    """Load a persona prompt from file and replace placeholders"""
    # Try to load the specific persona
    persona_content = load_prompt(f"personas/{persona_type}.md")
    if not persona_content:
        return None
    
    # Load the base prompt and substitute both problem and persona
    base_prompt = load_prompt("base_student.md", problem=problem, persona=persona_content)
    
    return base_prompt