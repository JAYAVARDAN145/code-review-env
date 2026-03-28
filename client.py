import requests

class CodeReviewClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def reset(self, task_level: str = "easy"):
        response = requests.post(
            f"{self.base_url}/reset",
            params={"task_level": task_level}
        )
        return response.json()

    def step(self, review: str, severity: str, line_number: int = None):
        payload = {
            "review": review,
            "severity": severity,
            "line_number": line_number,
        }
        response = requests.post(
            f"{self.base_url}/step",
            json=payload
        )
        return response.json()

    def state(self):
        response = requests.get(f"{self.base_url}/state")
        return response.json()