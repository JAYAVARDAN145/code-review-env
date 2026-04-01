from fastapi import FastAPI
from models import CodeReviewAction, CodeReviewObservation, CodeReviewState
from server.environment import CodeReviewEnvironment
import uvicorn

app = FastAPI(title="Code Review Environment")
env = CodeReviewEnvironment()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return {"tasks": env.all_tasks}

@app.post("/reset")
def reset(task_level: str = "easy") -> CodeReviewObservation:
    obs = env.reset(task_level=task_level)
    return obs

@app.post("/step")
def step(action: CodeReviewAction):
    if env.state.done:
        env.reset(task_level=env._task_level)
    obs, reward, done, grade = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "progress": grade["progress"],
        "penalty": grade["penalty"],
        "explanation": grade["explanation"],
        "matched_keywords": grade["matched_keywords"],
        "missed_keywords": grade["missed_keywords"],
    }

@app.get("/state")
def state() -> CodeReviewState:
    return env.state

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()