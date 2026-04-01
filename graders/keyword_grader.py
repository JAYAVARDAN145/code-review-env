from typing import List, Dict

def grade_review(review: str, expected_keywords: List[str]) -> Dict:
    """
    Grade a code review based on keyword matching.
    Returns detailed reward with explanation.
    """
    review_lower = review.lower()
    
    matched = []
    missed = []
    
    for kw in expected_keywords:
        if kw.lower() in review_lower:
            matched.append(kw)
        else:
            missed.append(kw)
    
    score = round(len(matched) / len(expected_keywords), 2)
    
    # Build explanation
    if score == 1.0:
        explanation = "Perfect review! All issues identified correctly."
    elif score >= 0.75:
        explanation = f"Good review! Missing: {', '.join(missed)}"
    elif score >= 0.5:
        explanation = f"Partial review. Found: {', '.join(matched)}. Missing: {', '.join(missed)}"
    elif score > 0:
        explanation = f"Weak review. Only found: {', '.join(matched)}. Missing: {', '.join(missed)}"
    else:
        explanation = "No issues identified. Try again with more specific details."
    
    # Penalty for very short reviews
    penalty = 0.0
    if len(review.split()) < 5:
        penalty = 0.2
        explanation += " Penalty: review too short."
    
    final_score = max(0.0, round(score - penalty, 2))
    
    return {
        "score": final_score,
        "progress": score,
        "penalty": penalty,
        "matched_keywords": matched,
        "missed_keywords": missed,
        "explanation": explanation
    }