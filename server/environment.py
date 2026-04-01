import uuid
from typing import Dict
from models import CodeReviewAction, CodeReviewObservation, CodeReviewState
from tasks.easy import EASY_TASK
from tasks.medium import MEDIUM_TASK
from tasks.hard import HARD_TASK
from tasks.expert import EXPERT_TASK
from graders.keyword_grader import grade_review

TASKS = {
    "easy": EASY_TASK,
    "medium": MEDIUM_TASK,
    "hard": HARD_TASK,
    "expert": EXPERT_TASK,
}

class CodeReviewEnvironment:
    def __init__(self):
        self._episode_id = str(uuid.uuid4())
        self._step_count = 0
        self._task_level = "easy"
        self._done = False
        self._score = 0.0
        self._last_grade = {}

    def reset(self, task_level: str = "easy") -> CodeReviewObservation:
        if task_level not in TASKS:
            raise ValueError(f"Unknown task level: {task_level}. Choose from {list(TASKS.keys())}")
        self._episode_id = str(uuid.uuid4())
        self._step_count = 0
        self._task_level = task_level
        self._done = False
        self._score = 0.0
        self._last_grade = {}
        task = TASKS[task_level]
        return CodeReviewObservation(
            code=task["code"],
            language=task["language"],
            task_description=task["description"],
            attempt=self._step_count,
            hints=task.get("hints"),
        )

    def step(self, action: CodeReviewAction) -> tuple:
        if self._done:
            self.reset(task_level=self._task_level)

        self._step_count += 1
        task = TASKS[self._task_level]

        grade = grade_review(action.review, task["expected_keywords"])
        self._score = grade["score"]
        self._last_grade = grade

        max_steps = task.get("max_steps", 3)
        if self._step_count >= max_steps or self._score == 1.0:
            self._done = True

        obs = CodeReviewObservation(
            code=task["code"],
            language=task["language"],
            task_description=task["description"],
            attempt=self._step_count,
            hints=task.get("hints"),
        )
        return obs, self._score, self._done, grade

    @property
    def state(self) -> CodeReviewState:
        return CodeReviewState(
            episode_id=self._episode_id,
            step_count=self._step_count,
            task_level=self._task_level,
            done=self._done,
            score=self._score,
        )

    @property
    def all_tasks(self):
        return [
            {
                "name": task["name"],
                "difficulty": task["difficulty"],
                "description": task["description"],
                "language": task["language"],
                "max_steps": task.get("max_steps", 3),
            }
            for task in TASKS.values()
        ]