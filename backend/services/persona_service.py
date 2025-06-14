from pathlib import Path
from typing import List, Optional

def get_personas_directory() -> Path:
    """Get the path to the personas directory"""
    backend_dir = Path(__file__).parent.parent
    return backend_dir / "prompts" / "personas"

def get_available_personas() -> List[str]:
    """Get list of available personas from the personas directory"""
    personas_dir = get_personas_directory()
    
    try:
        # Get all .md files and extract their names (without extension)
        persona_files = personas_dir.glob("*.md")
        return sorted([f.stem for f in persona_files])
    except Exception as e:
        print(f"Error listing personas: {e}")
        # Return empty list if directory scan fails
        return []

def load_persona_prompt(persona_type: str, math_problem: str) -> Optional[str]:
    """Load a persona prompt from file and replace placeholders"""
    personas_dir = get_personas_directory()
    persona_path = personas_dir / f"{persona_type}.md"
    
    # If exact match doesn't exist, try to find any .md file as fallback
    if not persona_path.exists():
        try:
            available_personas = list(personas_dir.glob("*.md"))
            if available_personas:
                persona_path = available_personas[0]
                print(f"Warning: Persona '{persona_type}' not found. Using '{persona_path.stem}' as fallback.")
            else:
                return None
        except Exception as e:
            print(f"Error finding personas: {e}")
            return None
    
    # Read the persona from file
    try:
        with open(persona_path, 'r') as f:
            persona_template = f.read()
        
        # Replace the {math_problem} placeholder
        persona_prompt = persona_template.replace("{math_problem}", math_problem)
        return persona_prompt
        
    except FileNotFoundError:
        print(f"Warning: Persona file {persona_path} not found.")
        return None