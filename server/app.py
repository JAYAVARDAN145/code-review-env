from fastapi import FastAPI
from models import CodeReviewAction, CodeReviewObservation, CodeReviewState
from server.environment import CodeReviewEnvironment

app = FastAPI(title="Code Review Environment")
env = CodeReviewEnvironment()

@app.post("/reset")
def reset(task_level: str = "easy") -> CodeReviewObservation:
    obs = env.reset(task_level=task_level)
    return obs

@app.post("/step")
def step(action: CodeReviewAction):
    if env.state.done:
        env.reset(task_level=env._task_level)
    obs, reward, done = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
    }

@app.get("/state")
def state() -> CodeReviewState:
    return env.state

@app.get("/health")
def health():
    return {"status": "ok"}