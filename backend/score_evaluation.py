import json
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

def calculate_user_stats(username):
        try:
            with open('data/users.json', 'r') as f:
                users = json.load(f)
                history = users[username]['history']

                if not history:
                    return {
                        "Overall Score": "No quizzes taken",
                        "Total Questions": "0",
                        "Quizzes Completed": "0"
                    }

                total_correct = 0
                total_questions = 0
                category_scores = {}

                for entry in history:
                    score_parts = entry['total_score'].split('/')
                    total_correct += int(score_parts[0])
                    total_questions += int(score_parts[1])

                    for cat in entry['categories']:
                        cat_name = cat['category']
                        cat_score = cat['score'].split('/')
                        if cat_name not in category_scores:
                            category_scores[cat_name] = {'correct': 0, 'total': 0}
                        category_scores[cat_name]['correct'] += int(cat_score[0])
                        category_scores[cat_name]['total'] += int(cat_score[1])

                stats = {
                    "Overall Score": f"{(total_correct/total_questions)*100:.1f}%",
                    "Total Questions": str(total_questions),
                    "Quizzes Completed": str(len(history))
                }

                for cat, scores in category_scores.items():
                    percentage = (scores['correct'] / scores['total']) * 100
                    stats[f"{cat}"] = f"{percentage:.1f}% ({scores['correct']}/{scores['total']})"

                return stats

        except Exception as e:
            print(f"Error calculating stats: {e}")
            return {
                "Error": "Could not load statistics"
            }
