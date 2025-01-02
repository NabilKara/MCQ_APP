import json
import os
import random

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

def prepare_quiz(self):
    """Prepare quiz questions based on selected categories, choosing 7 questions randomly."""
    self.questions = []
    self.score = []  # Initialize the score array

    # Combine all questions from selected categories
    for category in self.selected_categories:
        category_questions = self.all_questions.get(category, [])
        self.questions.extend([
            {
                "question": q["question"],
                "options": q["options"],
                "correct": q["correct"],
                "category": category
            }
            for q in category_questions
        ])
        self.score.append((category, 0, 0))  # (category, current_score, num_questions)

    # Shuffle and pick 7 random questions
    random.shuffle(self.questions)
    self.questions = self.questions[:7]  # Limit to 7 questions

    self.current_question = 0

# def prepare_quiz(self):
#     """Prepare quiz questions based on selected categories."""
#     self.questions = []
#     self.score = []  # Initialize the score array
#
#     for category in self.selected_categories:
#         category_questions = self.all_questions.get(category, [])
#         self.questions.extend([
#             {
#                 "question": q["question"],
#                 "options": q["options"],
#                 "correct": q["correct"],
#                 "category": category
#             }
#             for q in category_questions
#         ])
#         self.score.append((category, 0, 0))  # (category, current_score, num_questions)
#     self.current_question = 0