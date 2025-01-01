import json
import os

def load_questions():
    default_questions = {
        "Python": [
            {
                "question": "What is Python?",
                "options": ["Programming Language", "Snake", "Movie", "Game"],
                "correct": "1"
            }
        ],
        "Computer Science": [
            {
                "question": "What does CPU stand for?",
                "options": [
                    "Central Processing Unit",
                    "Central Programming Unit", 
                    "Control Processing Unit",
                    "Compute Program Unit"
                ],
                "correct": "1"
            }
        ],
        "Networking": [
            {
                "question": "What is the use of an IP address?",
                "options": [
                    "Identifies a device on a network",
                    "Encrypts data",
                    "Runs applications", 
                    "None of these"
                ],
                "correct": "1"
            }
        ]
    }
    
    try:
        with open('data/questions.json', 'r') as f:
            questions = json.load(f)
            return questions if questions else default_questions
    except (FileNotFoundError, json.JSONDecodeError):
        os.makedirs('data', exist_ok=True)
        with open('data/questions.json', 'w') as f:
            json.dump(default_questions, f, indent=4)
        return default_questions

def get_questions_for_categories(categories):
    questions = load_questions()
    selected_questions = []
    for category in categories:
        category_questions = questions.get(category, [])
        selected_questions.extend(category_questions)
    return selected_questions
