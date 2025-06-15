from typing import List
from .prompt_service import load_prompt, list_prompts_in_directory

def get_available_personas() -> List[str]:
    """Get list of available personas from the personas directory"""
    return list_prompts_in_directory("personas")

def load_persona_prompt(persona_type: str, problem: str) -> str:
    """Load a persona prompt from file and replace placeholders
    
    Raises:
        FileNotFoundError: If the persona file doesn't exist
        Exception: If there's an error loading the prompt
    """
    # Load the specific persona
    persona_content = load_prompt(f"personas/{persona_type}.md")
    
    # Load the base prompt and substitute both problem and persona
    base_prompt = load_prompt("base_student.md", problem=problem, persona=persona_content)
    
    return base_prompt