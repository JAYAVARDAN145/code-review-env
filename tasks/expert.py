EXPERT_TASK = {
    "name": "expert",
    "difficulty": "expert",
    "description": "Find all bugs including concurrency, memory leaks, and security issues.",
    "language": "python",
    "code": """
import threading
import requests

cache = {}

def fetch_user_data(user_id):
    if user_id in cache:
        return cache[user_id]
    response = requests.get(f"http://internal-api/users/{user_id}")
    data = response.json()
    cache[user_id] = data
    return data

def process_users(user_ids):
    threads = []
    results = []

    def worker(uid):
        data = fetch_user_data(uid)
        results.append(data)

    for uid in user_ids:
        t = threading.Thread(target=worker, args=(uid,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results

api_key = "sk-1234567890abcdef"
admin_password = "admin123"
""",
    "expected_keywords": [
        "race condition", "thread safe", "hardcoded",
        "secret", "lock", "ssrf", "internal", "cache"
    ],
    "hints": "Look for thread safety, hardcoded secrets, and SSRF vulnerability.",
    "max_steps": 4
}