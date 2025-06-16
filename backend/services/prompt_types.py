"""Type definitions for prompt parameters."""
from typing import TypedDict, List


class ConversationMessage(TypedDict):
    """Type for a single conversation message."""
    role: str
    content: str


class BaseStudentPromptParams(TypedDict):
    """Parameters for the base student prompt."""
    problem: str
    persona: str


class ScoringPromptParams(TypedDict):
    """Parameters for the scoring prompt."""
    conversation: List[ConversationMessage]
    problem: str
    persona_name: str
    categories_list: str