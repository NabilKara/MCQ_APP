def evaluate_performance(percentage):
    if percentage >= 90:
        return "Excellent! Outstanding performance!"
    elif percentage >= 80:
        return "Great job! Very good performance!"
    elif percentage >= 70:
        return "Good work! Keep it up!"
    elif percentage >= 60:
        return "Not bad! There's room for improvement."
    else:
        return "Keep practicing! You can do better!"

def calculate_percentage(score):
    """Calculate percentage score."""

    nb_questions = 0
    total_score = 0

    for i, (cat, current_score, num_questions) in enumerate(score):
        nb_questions += num_questions
        total_score += current_score

    if nb_questions == 0:
        return 0

    return (total_score / nb_questions) * 100
