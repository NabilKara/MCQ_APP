def evaluate_performance(percentage):
    if percentage >= 90:
        return "Excellent! Outstanding performance!"
    elif percentage >= 80:
        return "Great job! Very good performance!"
    elif percentage >= 70:
        return "Good work! Keep it up!"
    elif percentage >= 60:
        return "Not bad! Room for improvement."
    else:
        return "Keep practicing! You can do better!"

def calculate_percentage(score, total_questions):
    """Calculate percentage score."""
    if total_questions == 0:
        return 0
    return (score / total_questions) * 100
