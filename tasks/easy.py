EASY_TASK = {
    "name": "easy",
    "difficulty": "easy",
    "description": "Find the runtime error in this code.",
    "language": "python",
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
    "expected_keywords": ["division", "zero", "empty", "ZeroDivisionError"],
    "hints": "Look for what happens when an empty list is passed.",
    "max_steps": 3
}