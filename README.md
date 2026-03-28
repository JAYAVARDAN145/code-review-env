---
Title: Code Review Environment
emoji: 🔍
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Code Review Environment

A real-world OpenEnv environment where an AI agent reviews code
and identifies bugs, security issues, and performance problems.

## Motivation
Code review is a critical real-world task. This environment
trains agents to identify common issues in Python code,
from simple runtime errors to complex security vulnerabilities.

## Action Space
| Field | Type | Description |
|---|---|---|
| review | string | The review comment |
| severity | string | "low", "medium", "high" |
| line_number | integer | Optional line number |

## Observation Space
| Field | Type | Description |
|---|---|---|
| code | string | Code snippet to review |
| language | string | Programming language |
| task_description | string | What to look for |
| attempt | integer | Current attempt number |

## Tasks
| Task | Difficulty | Description |
|---|---|---|
| easy | Easy | Find runtime errors |
| medium | Medium | Find logic bugs and performance issues |
| hard | Hard | Find security vulnerabilities |

## Reward Function
- Score 0.0–1.0 based on keywords matched
- Partial credit for partial reviews
- Episode ends after 3 attempts or perfect score

## Setup

### Local
```bash
pip install fastapi uvicorn pydantic openenv-core
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### Docker
```bash
docker build -t code-review-env -f server/Dockerfile .
docker run -p 7860:7860 code-review-env
```

## Baseline Scores
| Task | Score |
|---|---|
| Easy | 0.75 |
| Medium | 0.50 |
| Hard | 0.40 |

## Usage
```python
from client import CodeReviewClient

env = CodeReviewClient(base_url="http://localhost:7860")
obs = env.reset(task_level="easy")
result = env.step(review="Division by zero error", severity="high")
```
