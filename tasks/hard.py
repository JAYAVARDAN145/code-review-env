HARD_TASK = {
    "name": "hard",
    "difficulty": "hard",
    "description": "Find all security vulnerabilities in this code.",
    "language": "python",
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
    "expected_keywords": ["injection", "sql", "password", "hash", "parameterized"],
    "hints": "Look for SQL injection and password handling issues.",
    "max_steps": 3
}