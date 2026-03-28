from pydantic import BaseModel
from typing import Optional

class CodeReviewAction(BaseModel):
    """Action taken by the agent — a code review comment"""
    review: str
    severity: str                  # "low", "medium", "high"
    line_number: Optional[int] = None

class CodeReviewObservation(BaseModel):
    """What the agent sees — a code snippet to review"""
    code: str
    language: str
    task_description: str
    attempt: int

class CodeReviewState(BaseModel):
    """Episode metadata"""
    episode_id: str
    step_count: int
    task_level: str                # "easy", "medium", "hard"
    done: bool
    score: float