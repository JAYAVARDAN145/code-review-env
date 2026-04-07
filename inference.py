"""
inference.py — OpenEnv Hackathon baseline agent
Repo: https://github.com/JAYAVARDAN145/code-review-env
HF Space: https://huggingface.co/spaces/Jayavardan/code-review-env

Prints the required structured output blocks to stdout:
  [START] task=<name>
  [STEP]  step=<n> reward=<r>
  [END]   task=<name> score=<total> steps=<n>
"""

import os
import sys
import json
import argparse
import requests
from openai import OpenAI

# ── Config ────────────────────────────────────────────────────────────────────
DEFAULT_URL  = "https://Jayavardan-code-review-env.hf.space"
TASKS        = ["easy", "medium", "hard"]
MODEL        = "gpt-4o-mini"           # cheap + fast; swap for gpt-4o if you want

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ── OpenEnv HTTP helpers ───────────────────────────────────────────────────────
def reset(base_url: str, task_id: str) -> dict:
    r = requests.post(
        f"{base_url}/reset",
        json={"task_id": task_id},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()

def step(base_url: str, action: dict) -> dict:
    r = requests.post(
        f"{base_url}/step",
        json={"action": action},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()

# ── LLM agent ─────────────────────────────────────────────────────────────────
def build_prompt(observation: dict) -> str:
    """Convert the observation dict into a plain-English prompt for the LLM."""
    obs_text = json.dumps(observation, indent=2)
    return f"""You are an expert code reviewer.

Here is the current environment observation:
{obs_text}

Respond with a JSON object containing your review action.
The action must match the action schema for this environment.
Return ONLY valid JSON, nothing else."""


def llm_action(observation: dict, action_schema: dict) -> dict:
    """Ask GPT to produce an action given the current observation."""
    prompt = build_prompt(observation)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    raw = response.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: return a minimal safe action
        return {"review": "no issues found", "severity": "low", "confidence": 0.5}


def get_action_schema(base_url: str) -> dict:
    """Fetch the action schema from the /tasks endpoint."""
    try:
        r = requests.get(f"{base_url}/tasks", timeout=15)
        r.raise_for_status()
        data = r.json()
        return data.get("action_schema", {})
    except Exception:
        return {}


# ── Main episode runner ────────────────────────────────────────────────────────
def run_task(base_url: str, task_id: str) -> float:
    """
    Run one complete episode for the given task.
    Prints [START], one [STEP] per step, and [END] to stdout.
    Returns total episode reward.
    """
    # ── [START] ────────────────────────────────────────────────────────────────
    print(f"[START] task={task_id}", flush=True)

    action_schema = get_action_schema(base_url)

    # Reset the environment
    reset_result = reset(base_url, task_id)
    observation  = reset_result.get("observation", reset_result)

    total_reward = 0.0
    step_num     = 0
    done         = False

    while not done:
        step_num += 1

        # Agent picks an action
        action = llm_action(observation, action_schema)

        # Send action to environment
        step_result = step(base_url, action)

        reward      = float(step_result.get("reward", 0.0))
        done        = bool(step_result.get("done", True))
        observation = step_result.get("observation", {})
        total_reward += reward

        # ── [STEP] ─────────────────────────────────────────────────────────────
        print(f"[STEP] step={step_num} reward={reward:.4f}", flush=True)

        # Safety cap: never loop more than 50 steps
        if step_num >= 50:
            break

    # Normalise score to [0, 1]
    score = max(0.0, min(1.0, total_reward))

    # ── [END] ──────────────────────────────────────────────────────────────────
    print(f"[END] task={task_id} score={score:.4f} steps={step_num}", flush=True)

    return score


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Code Review Env — baseline inference")
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help="Base URL of your deployed HF Space (no trailing slash)",
    )
    parser.add_argument(
        "--tasks",
        nargs="+",
        default=TASKS,
        choices=TASKS,
        help="Which tasks to run (default: all three)",
    )
    args = parser.parse_args()

    base_url = args.url.rstrip("/")
    results  = {}

    for task_id in args.tasks:
        try:
            score = run_task(base_url, task_id)
            results[task_id] = score
        except Exception as e:
            # Still print [END] with score=0 so the validator sees the block
            print(f"[END] task={task_id} score=0.0000 steps=0", flush=True)
            print(f"ERROR running task {task_id}: {e}", file=sys.stderr, flush=True)
            results[task_id] = 0.0

    # Summary (not parsed by validator, just useful for you)
    print("\n=== Baseline Results ===", flush=True)
    for task_id, score in results.items():
        print(f"  {task_id:8s}: {score:.4f}", flush=True)
    print(f"  average : {sum(results.values()) / len(results):.4f}", flush=True)


if __name__ == "__main__":
    main()