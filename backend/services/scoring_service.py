import json
from pathlib import Path
from typing import List, Dict, Any

def get_scoring_categories() -> List[Dict[str, Any]]:
    """Load scoring categories from configuration file"""
    config_path = Path(__file__).parent.parent / "config" / "scoring_categories.json"
    
    with open(config_path, 'r') as f:
        data = json.load(f)
        categories = data.get('categories', [])
        if not categories:
            raise ValueError("No categories found in scoring configuration")
        return categories

def get_category_keys() -> List[str]:
    """Get just the keys of all scoring categories"""
    return [cat['key'] for cat in get_scoring_categories()]

def generate_categories_list() -> str:
    """Generate a simple list of categories for evaluation"""
    categories = get_scoring_categories()
    category_lines = []
    
    for cat in categories:
        # Include description if available
        description = cat.get('description', '')
        if description:
            category_lines.append(f"- {cat['key']}: {cat['label']} - {description}")
        else:
            category_lines.append(f"- {cat['key']}: {cat['label']}")
    
    return "\n".join(category_lines)