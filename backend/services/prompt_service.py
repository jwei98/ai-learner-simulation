from pathlib import Path
from typing import Optional, Dict, Any

def get_prompts_directory() -> Path:
    """Get the path to the prompts directory"""
    backend_dir = Path(__file__).parent.parent
    return backend_dir / "prompts"

def load_prompt(prompt_path: str, **kwargs: Any) -> Optional[str]:
    """
    Load a prompt from file and replace placeholders.
    
    Args:
        prompt_path: Relative path from the prompts directory (e.g., "personas/struggling_sam.md")
        **kwargs: Key-value pairs for placeholder replacement
    
    Returns:
        The loaded prompt with placeholders replaced, or None if loading fails
    """
    prompts_dir = get_prompts_directory()
    full_path = prompts_dir / prompt_path
    
    try:
        with open(full_path, 'r') as f:
            prompt_template = f.read()
        
        # Replace placeholders with provided values
        for key, value in kwargs.items():
            # Use double braces for the placeholder
            placeholder = "{{" + key + "}}"
            prompt_template = prompt_template.replace(placeholder, str(value))
        
        return prompt_template
        
    except FileNotFoundError:
        print(f"Warning: Prompt file {full_path} not found.")
        return None
    except Exception as e:
        print(f"Error loading prompt from {full_path}: {e}")
        return None

def list_prompts_in_directory(subdirectory: str = "") -> list[str]:
    """
    List all .md files in a given subdirectory of the prompts folder.
    
    Args:
        subdirectory: Subdirectory path relative to prompts folder (e.g., "personas")
    
    Returns:
        List of prompt file names (without extension)
    """
    prompts_dir = get_prompts_directory()
    target_dir = prompts_dir / subdirectory if subdirectory else prompts_dir
    
    try:
        prompt_files = target_dir.glob("*.md")
        return sorted([f.stem for f in prompt_files])
    except Exception as e:
        print(f"Error listing prompts in {target_dir}: {e}")
        return []