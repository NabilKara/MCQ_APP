import json
import os
import random

def load_questions():
    """
    Load the quiz questions from the JSON file. If the file does not exist or is empty, return a default set of questions.
    """
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
    """
    Prepare quiz questions based on selected categories, choosing a balanced selection 
    of questions from each category up to a total of 7 questions, with randomized options.
    """
    self.questions = []
    self.score = []  # Initialize the score array
    
    if not self.selected_categories:
        return
        
    # Calculate how many questions to take from each category
    num_categories = len(self.selected_categories)
    questions_per_category = 7 // num_categories  # Integer division
    remaining_questions = 7 % num_categories
    
    # Get questions from each category
    for category in self.selected_categories:
        category_questions = self.all_questions.get(category, [])
        
        # Determine number of questions to take from this category
        num_to_take = questions_per_category
        if remaining_questions > 0:
            num_to_take += 1
            remaining_questions -= 1
            
        # Randomly select questions from this category
        selected = random.sample(
            category_questions,
            min(num_to_take, len(category_questions))
        )

        # Add category information to each question and randomize options
        for q in selected:
            # Create pairs of options with their indices
            options = q["options"]
            correct_idx = int(q["correct"]) - 1
            option_pairs = list(enumerate(options))

            # Shuffle the pairs
            random.shuffle(option_pairs)
            
            # Unpack the shuffled pairs
            indices, shuffled_options = zip(*option_pairs)
            
            # Find where the correct answer went
            new_correct = str(indices.index(correct_idx) + 1)
            
            self.questions.append({
                "question": q["question"],
                "options": list(shuffled_options),
                "correct": new_correct,
                "category": category
            })
            
        # Initialize score tracking for this category
        self.score.append((category, 0, 0))  # (category, current_score, num_questions)
    
    # Shuffle the final question list
    random.shuffle(self.questions)
    
    # Ensure we don't exceed 7 questions total
    self.questions = self.questions[:7]
    self.current_question = 0