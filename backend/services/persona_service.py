from typing import List
from .prompt_service import list_available_personas, generate_base_student_prompt, load_persona_content
from .prompt_types import BaseStudentPromptParams

def get_available_personas() -> List[str]:
    """Get list of available personas"""
    return list_available_personas()

def load_persona_prompt(persona_type: str, problem: str) -> str:
    """Load a persona prompt and generate the full prompt with parameters
    
    Args:
        persona_type: The type of persona (e.g., 'anxious_alex')
        problem: The problem text to include in the prompt
        
    Returns:
        The formatted prompt string
        
    Raises:
        ValueError: If the persona type is not found
    """
    # Load the specific persona content
    persona_content = load_persona_content(persona_type)
    
    # Generate the base prompt with typed parameters
    params: BaseStudentPromptParams = {
        'problem': problem,
        'persona': persona_content
    }
    
    return generate_base_student_prompt(params)