import uuid
from models import CodeReviewAction, CodeReviewObservation, CodeReviewState

# Tasks with code snippets and expected issues
TASKS = {
    "easy": {
        "code": """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total = total + num
    average = total / len(numbers)
    return average

result = calculate_average([])
print(result)
""",
        "language": "python",
        "task_description": "Find the syntax or runtime error in this code.",
        "expected_keywords": ["division", "zero", "empty", "ZeroDivisionError"],
    },
    "medium": {
        "code": """
def find_duplicates(lst):
    duplicates = []
    for i in range(len(lst)):
        for j in range(len(lst)):
            if lst[i] == lst[j]:
                duplicates.append(lst[i])
    return duplicates

print(find_duplicates([1, 2, 3, 2, 4]))
""",
        "language": "python",
        "task_description": "Find the logic bug and performance issue in this code.",
        "expected_keywords": ["duplicate", "itself", "i != j", "O(n^2)", "inefficient"],
    },
    "hard": {
        "code": """
import sqlite3

def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()

def login(username, password):
    user = get_user(username)
    if user and user[2] == password:
        return True
    return False
""",
        "language": "python",
        "task_description": "Find all security vulnerabilities in this code.",
        "expected_keywords": ["injection", "sql", "password", "hash", "parameterized"],
    },
}

class CodeReviewEnvironment:
    def __init__(self):
        self._episode_id = str(uuid.uuid4())
        self._step_count = 0
        self._task_level = "easy"
        self._done = False
        self._score = 0.0

    def reset(self, task_level: str = "easy") -> CodeReviewObservation:
        self._episode_id = str(uuid.uuid4())
        self._step_count = 0
        self._task_level = task_level
        self._done = False
        self._score = 0.0
        task = TASKS[task_level]
        return CodeReviewObservation(
            code=task["code"],
            language=task["language"],
            task_description=task["task_description"],
            attempt=self._step_count,
        )

    def step(self, action: CodeReviewAction) -> tuple:
        if self._done:
            raise ValueError("Episode is done. Call reset() first.")

        self._step_count += 1
        task = TASKS[self._task_level]
        review_lower = action.review.lower()

        # Score based on how many expected keywords are found
        matched = sum(
            1 for kw in task["expected_keywords"]
            if kw.lower() in review_lower
        )
        self._score = round(matched / len(task["expected_keywords"]), 2)

        # End episode after 3 attempts or perfect score
        if self._step_count >= 3 or self._score == 1.0:
            self._done = True

        obs = CodeReviewObservation(
            code=task["code"],
            language=task["language"],
            task_description=task["task_description"],
            attempt=self._step_count,
        )
        return obs, self._score, self._done

    @property
    def state(self) -> CodeReviewState:
        return CodeReviewState(
            episode_id=self._episode_id,
            step_count=self._step_count,
            task_level=self._task_level,
            done=self._done,
            score=self._score,
        )