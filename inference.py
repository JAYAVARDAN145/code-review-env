"""
Inference Script - Code Review Environment
- API_BASE_URL: The API endpoint for the LLM
- MODEL_NAME: The model identifier to use for inference
- HF_TOKEN: Your Hugging Face API key
"""

import os
from openai import OpenAI
from client import CodeReviewClient

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct")
ENV_URL = os.getenv("ENV_URL", "https://Jayavardan-code-review-env.hf.space")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
env = CodeReviewClient(base_url=ENV_URL)

SYSTEM_PROMPT = """You are an expert code reviewer.
Review the given code and identify all issues including:
- Runtime errors and exceptions
- Logic bugs and incorrect behavior
- Security vulnerabilities
- Performance problems
Be specific and mention exact error types like ZeroDivisionError, SQL injection etc."""

def run_task(task_level: str) -> float:
    print(f"\n--- Task: {task_level.upper()} ---")
    obs = env.reset(task_level=task_level)
    print(f"Code:\n{obs['code']}")
    print(f"Task: {obs['task_description']}")

    score = 0.0
    for attempt in range(3):
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"""
Review this {obs['language']} code:

{obs['code']}

Task: {obs['task_description']}

Provide a detailed code review identifying all issues.
"""}
            ],
            max_tokens=500,
            temperature=0.2,
        )

        review_text = response.choices[0].message.content
        print(f"\nAttempt {attempt + 1}:\n{review_text[:200]}...")

        result = env.step(
            review=review_text,
            severity="high",
        )

        score = result["reward"]
        done = result["done"]
        print(f"Score: {score}, Done: {done}")

        if done:
            break

    return score

def main():
    print("=== Code Review Environment Baseline ===")
    scores = {}

    for level in ["easy", "medium", "hard"]:
        scores[level] = run_task(level)

    print("\n=== Final Scores ===")
    for level, score in scores.items():
        print(f"{level.upper()}: {score:.2f}")

    avg = sum(scores.values()) / len(scores)
    print(f"AVERAGE: {avg:.2f}")

if __name__ == "__main__":
    main()