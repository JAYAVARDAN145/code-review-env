MEDIUM_TASK = {
    "name": "medium",
    "difficulty": "medium",
    "description": "Find the logic bug and performance issue in this code.",
    "language": "python",
    "code": """
def find_duplicates(lst):
    duplicates = []
    for i in range(len(lst)):
        for j in range(len(lst)):
            if lst[i] == lst[j]:
                duplicates.append(lst[i])
    return duplicates

print(find_duplicates([1, 2, 3, 2, 4]))
""",
    "expected_keywords": ["duplicate", "itself", "i != j", "O(n^2)", "inefficient"],
    "hints": "Look for self-comparison and nested loop complexity.",
    "max_steps": 3
}