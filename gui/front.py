import customtkinter as ctk
import json
from datetime import datetime
import os

class MCQApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MCQ Quiz App")
        self.geometry("600x400")
        
        self.configure(fg_color="#3f51b5")
        
        # Initialize instance variables
        self.current_user = None
        self.score = 0
        self.current_question = 0
        self.selected_categories = []
        self.questions = []
        
        # Ensure the data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Load questions
        self.all_questions = self.load_questions()
        
        self.frames = {
            "login": LoginFrame,
            "welcome": WelcomeFrame,
            "mode": ModeFrame,
            "categories": CategoryFrame,
            "history": HistoryFrame,
            "quiz": QuizFrame,
            "wrong": WrongFrame,
            "score": ScoreFrame
        }
        
        self.current_frame = None
        self.show_frame("login")
    
    def load_questions(self):
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
                loaded_questions = json.load(f)
                if not loaded_questions:
                    return default_questions
                return loaded_questions
        except (FileNotFoundError, json.JSONDecodeError):
            with open('data/questions.json', 'w') as f:
                json.dump(default_questions, f, indent=4)
            return default_questions
    
    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.destroy()
        
        Frame = self.frames[frame_name]
        self.current_frame = Frame(self)
        self.current_frame.pack(fill="both", expand=True)
    
    def prepare_quiz(self):
        """Prepare quiz questions based on selected categories."""
        self.questions = []
        for category in self.selected_categories:
            category_questions = self.all_questions.get(category, [])
            self.questions.extend([
                {
                    "question": q["question"],
                    "options": q["options"],
                    "correct": q["correct"]
                }
                for q in category_questions
            ])
        self.current_question = 0
        self.score = 0

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        
        greeting = ctk.CTkLabel(
            self,
            text="Welcome to the MCQ Quiz App!",
            text_color="white",
            font=("Arial", 24, "bold")
        )
        greeting.pack(pady=(50, 20))
        
        login_container = ctk.CTkFrame(self, fg_color="transparent")
        login_container.pack(pady=20)
        
        self.username_entry = ctk.CTkEntry(
            login_container,
            placeholder_text="Enter username",
            width=250,
            fg_color="gray70",
            text_color="black"

        )
        self.username_entry.pack(pady=(0, 30))
        self.username_entry.bind('<Return>', lambda e: self.check_user())
        
        self.login_button = ctk.CTkButton(
            login_container,
            text="Login",
            command=self.check_user,
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=120,
            height=32,
            text_color="white",
            font=("Arial", 14),
            corner_radius=8
        )
        self.login_button.pack(pady=(0, 10))
    
    def check_user(self):
        username = self.username_entry.get().strip()
        if not username:
            warning = ctk.CTkLabel(
                self,
                text="Please enter a username",
                text_color="yellow",
                font=("Arial", 14)
            )
            warning.pack(pady=10)
            self.after(2000, warning.destroy)
            return
        
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {}
        
        if username not in users:
            users[username] = []
            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4)
        
        self.master.current_user = username
        self.master.show_frame("mode" if not users[username] else "welcome")

class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        
        ctk.CTkLabel(
            self,
            text=f"Welcome back, {parent.current_user}!",
            text_color="white",
            font=("Arial", 24, "bold")
        ).pack(pady=(50, 20))
        
        history_frame = ctk.CTkFrame(self, fg_color="transparent")
        history_frame.pack(pady=20)
        
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
                history = users[parent.current_user]
                
                if history:
                    ctk.CTkLabel(
                        history_frame,
                        text="Your previous attempts:",
                        text_color="white",
                        font=("Arial", 18)
                    ).pack(pady=(0, 10))
                    
                    for entry in history[-3:]:
                        ctk.CTkLabel(
                            history_frame,
                            text=f"Date: {entry['date']}, Score: {entry['score']}",
                            text_color="white",
                            font=("Arial", 14)
                        ).pack(pady=5)
        except:
            pass
        
        ctk.CTkButton(
            self,
            text="Start Quiz",
            fg_color="green",
            font=("Arial", 14),
            command=lambda: parent.show_frame("mode")
        ).pack(pady=40)
        
        ctk.CTkButton(
            self,
            text="Change User",
            fg_color="red",
            font=("Arial", 14),
            command=lambda: parent.show_frame("login")
        ).pack(pady=(0, 20))

class ModeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        
        title = ctk.CTkLabel(
            self,
            text="Choose your mode:",
            text_color="white",
            font=("Arial", 20)
        )
        title.pack(pady=(100, 20))
        
        self.mode_var = ctk.StringVar()
        
        online = ctk.CTkRadioButton(
            self,
            text="Online Mode",
            variable=self.mode_var,
            value="online",
            text_color="white",
            font=("Arial", 16)
        )
        online.pack(pady=5)
        
        offline = ctk.CTkRadioButton(
            self,
            text="Offline Mode",
            variable=self.mode_var,
            value="offline",
            text_color="white",
            font=("Arial", 16)
        )
        offline.pack(pady=5)
        
        ctk.CTkButton(
            self,
            text="Continue",
            fg_color="green",
            font=("Arial", 14),
            command=lambda: parent.show_frame("categories")
        ).pack(pady=(20, 0))
        
        ctk.CTkButton(
            self,
            text="Return",
            fg_color="red",
            font=("Arial", 14),
            command=lambda: parent.show_frame("welcome")
        ).pack(pady=10)

class CategoryFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        
        title = ctk.CTkLabel(
            self,
            text="Select Categories:",
            text_color="white",
            font=("Arial", 20)
        )
        title.pack(pady=(50, 20))
        
        self.category_vars = {}
        categories = list(parent.all_questions.keys())
        
        checkbox_frame = ctk.CTkFrame(self, fg_color="transparent")
        checkbox_frame.pack(pady=20)
        
        for category in categories:
            var = ctk.BooleanVar()
            self.category_vars[category] = var
            ctk.CTkCheckBox(
                checkbox_frame,
                text=category,
                variable=var,
                text_color="white",
                font=("Arial", 14)
            ).pack(pady=10, padx=20, anchor="w")
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        ctk.CTkButton(
            btn_frame,
            text="Start Quiz",
            fg_color="green",
            font=("Arial", 14),
            command=self.start_quiz
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Change Mode",
            fg_color="red",
            font=("Arial", 14),
            command=lambda: parent.show_frame("mode")
        ).pack(side="left", padx=10)
    
    def start_quiz(self):
        selected = [cat for cat, var in self.category_vars.items() if var.get()]
        if not selected:
            warning = ctk.CTkLabel(
                self,
                text="Please select at least one category",
                text_color="yellow",
                font=("Arial", 14)
            )
            warning.pack(pady=10)
            self.after(2000, warning.destroy)
            return
        
        self.master.selected_categories = selected
        self.master.prepare_quiz()
        self.master.show_frame("quiz")

class QuizFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        
        self.parent = parent
        self.answer_var = ctk.StringVar()
        
        if not parent.questions:
            ctk.CTkLabel(
                self,
                text="No questions available",
                text_color="yellow",
                font=("Arial", 18)
            ).pack(pady=50)
            return
        
        question = parent.questions[parent.current_question]
        
        title = ctk.CTkLabel(
            self,
            text=question["question"],
            text_color="white",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(50, 30))
        
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.pack(pady=10)
        
        for i, option in enumerate(question["options"], 1):
            ctk.CTkRadioButton(
                options_frame,
                text=option,
                variable=self.answer_var,
                value=str(i),
                text_color="white",
                font=("Arial", 14)
            ).pack(pady=10, padx=(50, 0), anchor="w")
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=40)
        
        ctk.CTkButton(
            btn_frame,
            text="Submit Answer",
            fg_color="green",
            font=("Arial", 14),
            command=self.check_answer
        ).pack(side="left", padx=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Quit Quiz",
            fg_color="red",
            font=("Arial", 14),
            command=lambda: parent.show_frame("mode")
        ).pack(side="left", padx=20)
    
    def check_answer(self):
        question = self.parent.questions[self.parent.current_question]
        if self.answer_var.get() == question["correct"]:
            self.parent.score += 1
            self.next_question()
        else:
            self.parent.show_frame("wrong")
    
    def next_question(self):
        self.parent.current_question += 1
        if self.parent.current_question >= len(self.parent.questions):
            self.parent.show_frame("score")
        else:
            self.parent.show_frame("quiz")

class WrongFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        
        ctk.CTkLabel(
            self,
            text="Incorrect Answer!",
            text_color="red",
            font=("Arial", 24, "bold")
        ).pack(pady=(100, 20))
        
        ctk.CTkLabel(
            self,
            text="The correct answer is:",
            text_color="white",
            font=("Arial", 16)
        ).pack(pady=5)
        
        question = parent.questions[parent.current_question]
        correct_answer = question["options"][int(question["correct"]) - 1]
        
        ctk.CTkLabel(
            self,
            text=correct_answer,
            text_color="#4CAF50",
            font=("Arial", 18, "bold")
        ).pack(pady=10)
        
        ctk.CTkButton(
            self,
            text="Next Question",
            fg_color="green",
            font=("Arial", 14),
            command=self.next_question
        ).pack(pady=40)
    
    def next_question(self):
        self.master.current_question += 1
        if self.master.current_question >= len(self.master.questions):
            self.master.show_frame("score")
        else:
            self.master.show_frame("quiz")
class HistoryFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        
        # Title
        ctk.CTkLabel(
            self,
            text=f"Quiz History for {parent.current_user}",
            text_color="white",
            font=("Arial", 24, "bold")
        ).pack(pady=(30, 20))
        
        # Create scrollable frame for history entries
        history_container = ctk.CTkScrollableFrame(
            self,
            width=500,
            height=250,
            fg_color="transparent"
        )
        history_container.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Load and display history
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
                history = users.get(parent.current_user, [])
                
                if not history:
                    ctk.CTkLabel(
                        history_container,
                        text="No quiz history available",
                        text_color="yellow",
                        font=("Arial", 16)
                    ).pack(pady=20)
                else:
                    # Display each history entry
                    for entry in reversed(history):
                        entry_frame = ctk.CTkFrame(
                            history_container,
                            fg_color="#1a237e",
                            corner_radius=10
                        )
                        entry_frame.pack(pady=5, padx=10, fill="x")
                        
                        # Date
                        ctk.CTkLabel(
                            entry_frame,
                            text=f"Date: {entry['date']}",
                            text_color="white",
                            font=("Arial", 14)
                        ).pack(pady=(5, 0), padx=10, anchor="w")
                        
                        # Score
                        ctk.CTkLabel(
                            entry_frame,
                            text=f"Score: {entry['score']}",
                            text_color="#4CAF50",
                            font=("Arial", 14, "bold")
                        ).pack(pady=(0, 5), padx=10, anchor="w")
                        
                        # Categories
                        if 'categories' in entry:
                            categories_text = ", ".join(entry['categories'])
                            ctk.CTkLabel(
                                entry_frame,
                                text=f"Categories: {categories_text}",
                                text_color="white",
                                font=("Arial", 12)
                            ).pack(pady=(0, 5), padx=10, anchor="w")
                        
                        # Add separator except for last item
                        if entry != history[-1]:
                            ctk.CTkFrame(
                                history_container,
                                height=1,
                                fg_color="gray70"
                            ).pack(fill="x", pady=5)
                            
        except Exception as e:
            ctk.CTkLabel(
                history_container,
                text="Error loading history",
                text_color="red",
                font=("Arial", 16)
            ).pack(pady=20)
            print(f"Error loading history: {e}")
        
        # Button frame
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        # Add buttons
        ctk.CTkButton(
            btn_frame,
            text="New Quiz",
            fg_color="green",
            font=("Arial", 14),
            command=lambda: parent.show_frame("mode")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Return to Welcome",
            fg_color="#FF9800",
            font=("Arial", 14),
            command=lambda: parent.show_frame("welcome")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Change User",
            fg_color="red",
            font=("Arial", 14),
            command=lambda: parent.show_frame("login")
        ).pack(side="left", padx=10)

class ScoreFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        
        # Calculate percentage score
        total_questions = len(parent.questions)
        percentage = (parent.score / total_questions) * 100 if total_questions > 0 else 0
        
        # Display score
        ctk.CTkLabel(
            self,
            text="Quiz Complete!",
            text_color="white",
            font=("Arial", 24, "bold")
        ).pack(pady=(50, 20))
        
        ctk.CTkLabel(
            self,
            text=f"Your Score: {parent.score}/{total_questions}",
            text_color="white",
            font=("Arial", 20)
        ).pack(pady=10)
        
        ctk.CTkLabel(
            self,
            text=f"Percentage: {percentage:.1f}%",
            text_color="white",
            font=("Arial", 20)
        ).pack(pady=10)
        
        # Display performance message based on score
        performance_text = self.get_performance_message(percentage)
        ctk.CTkLabel(
            self,
            text=performance_text,
            text_color="#4CAF50",
            font=("Arial", 18)
        ).pack(pady=20)
        
        # Save score to user history
        self.save_score(parent)
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=40)
        
        ctk.CTkButton(
            btn_frame,
            text="View History",
            fg_color="#FF9800",
            font=("Arial", 14),
            command=lambda: parent.show_frame("history")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Try Again",
            fg_color="green",
            font=("Arial", 14),
            command=lambda: parent.show_frame("mode")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Change User",
            fg_color="red",
            font=("Arial", 14),
            command=lambda: parent.show_frame("login")
        ).pack(side="left", padx=10)
    
    def get_performance_message(self, percentage):
        """Return a performance message based on the score percentage."""
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
    
    def save_score(self, parent):
        """Save the quiz score to user history."""
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
            
            # Create score entry
            score_entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "score": f"{parent.score}/{len(parent.questions)}",
                "categories": parent.selected_categories
            }
            
            # Add to user's history
            if parent.current_user not in users:
                users[parent.current_user] = []
            users[parent.current_user].append(score_entry)
            
            # Save updated history
            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4)
                
        except Exception as e:
            print(f"Error saving score: {e}")

if __name__ == "__main__":
    app = MCQApp()
    app.mainloop()