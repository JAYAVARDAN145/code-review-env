---
Title: Code Review Environment
emoji: 🔍
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
---

# Code Review Environment

A real-world OpenEnv environment where an AI agent reviews code and identifies bugs, security issues, and performance problems.

## Motivation

Code review is a critical real-world task performed by developers every day. This environment trains and evaluates AI agents on their ability to identify common issues in Python code — from simple runtime errors to complex concurrency and security vulnerabilities.

## Action Space

| Field | Type | Description |
|---|---|---|
| review | string | The review comment identifying issues |
| severity | string | "low", "medium", "high" |
| line_number | integer | Optional line number of the issue |

## Observation Space

| Field | Type | Description |
|---|---|---|
| code | string | Code snippet to review |
| language | string | Programming language |
| task_description | string | What to look for |
| attempt | integer | Current attempt number |
| hints | string | Optional hints for the agent |

## Tasks

| Task | Difficulty | Description | Max Steps |
|---|---|---|---|
| easy | Easy | Find runtime errors (ZeroDivisionError) | 3 |
| medium | Medium | Find logic bugs and performance issues (O(n^2)) | 3 |
| hard | Hard | Find security vulnerabilities (SQL injection) | 3 |
| expert | Expert | Find concurrency, memory, and security issues | 4 |

## Reward Function

- Score 0.0–1.0 based on keywords matched
- Partial credit for partial reviews
- Penalty for very short reviews (< 5 words)
- Detailed explanation of what was found and missed
- Episode ends after max steps or perfect score

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| /health | GET | Health check |
| /tasks | GET | List all available tasks |
| /reset | POST | Start new episode |
| /step | POST | Submit a review |
| /state | GET | Get episode metadata |

## Setup

### Local
```bash
pip install -r requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### Docker
```bash
docker build -t code-review-env .
docker run -p 7860:7860 code-review-env
```

## Baseline Scores

| Task | Score |
|---|---|
| Easy | 1.00 |
| Medium | 0.80 |
| Hard | 0.60 |
| Expert | 0.50 |

## Environment Variables

| Variable | Description |
|---|---|
| API_BASE_URL | LLM API endpoint |
| MODEL_NAME | Model identifier |
| HF_TOKEN | HuggingFace token |

## Usage
```python
from client import CodeReviewClient

env = CodeReviewClient(base_url="http://localhost:7860")

# List all tasks
tasks = env.get_tasks()

# Reset environment
obs = env.reset(task_level="easy")

# Submit review
result = env.step(
    review="ZeroDivisionError when empty list passed",
    severity="high"
)
print(f"Score: {result['reward']}")
print(f"Explanation: {result['explanation']}")
```

## Live Links

- HuggingFace Space: https://huggingface.co/spaces/Jayavardan/code-review-env
- GitHub: https://github.com/JAYAVARDAN145/code-review-env