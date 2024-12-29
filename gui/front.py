import customtkinter as ctk
import json
from datetime import datetime

class MCQApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MCQ Quiz App")
        self.geometry("600x400")
        
        self.configure(fg_color="#3f51b5")
        
        self.current_user = None
        self.score = 0
        self.current_question = 0
        self.selected_categories = []
        self.questions = []
        
        # Load questions from JSON file or fallback to default
        self.all_questions = self.load_questions()
        
        self.frames = {
            "login": LoginFrame,
            "welcome": WelcomeFrame,
            "mode": ModeFrame,
            "categories": CategoryFrame,  # Added CategoryFrame
            "history": HistoryFrame,
            "quiz": QuizFrame,
            "wrong": WrongFrame,
            "score": ScoreFrame
        }
        
        self.current_frame = None
        self.show_frame("login")
    
    def load_questions(self):
        try:
            with open('questions.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
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
            for q in category_questions:
                formatted_q = {
                    "question": q["question"],
                    "options": q["options"],
                    "correct": q["correct"]
                }
                self.questions.append(formatted_q)
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
        greeting.pack(pady=(100, 20))
        
        self.username_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter username",
            width=200,
            fg_color="gray70"
        )
        self.username_entry.pack(pady=20)
        self.username_entry.bind('<Return>', lambda e: self.check_user())
    
    def check_user(self):
        username = self.username_entry.get()
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}
        
        if username not in users:
            users[username] = []
            with open('users.json', 'w') as f:
                json.dump(users, f)
        
        self.master.current_user = username
        
        # Show mode directly if no history, otherwise show welcome screen
        if not users[username]:
            self.master.show_frame("mode")
        else:
            self.master.show_frame("welcome")

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
        
        # Create a frame for checkboxes
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
        
        # Button frame
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
            # Show warning if no categories selected
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

class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        
        # Welcome message
        ctk.CTkLabel(
            self,
            text=f"Welcome, {parent.current_user}!",
            text_color="white",
            font=("Arial", 24, "bold")
        ).pack(pady=(50, 20))
        
        # Create a frame for history
        history_frame = ctk.CTkFrame(self, fg_color="transparent")
        history_frame.pack(pady=20)
        
        # Try to load and display user history
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
                history = users[parent.current_user]
                
                if history:  # Only show history if it exists
                    ctk.CTkLabel(
                        history_frame,
                        text="Your previous attempts:",
                        text_color="white",
                        font=("Arial", 18)
                    ).pack(pady=(0, 10))
                    
                    for entry in history[-3:]:  # Show last 3 entries
                        ctk.CTkLabel(
                            history_frame,
                            text=f"Date: {entry['date']}, Score: {entry['score']}",
                            text_color="white",
                            font=("Arial", 14)
                        ).pack(pady=5)
        except:
            pass
        
        # Continue button
        ctk.CTkButton(
            self,
            text="Start Quiz",
            fg_color="green",
            font=("Arial", 14),
            command=lambda: parent.show_frame("mode")
        ).pack(pady=40)
        
        # Return button
        ctk.CTkButton(
            self,
            text="Change User",
            fg_color="red",
            font=("Arial", 14),
            command=lambda: parent.show_frame("login")
        ).pack(pady=(0, 20))

# [Rest of the classes remain the same as in the previous version]
class ModeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        
        title = ctk.CTkLabel(
            self, 
            text="Choose the mode:", 
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
            font=("Arial", 16),
            command=lambda: parent.show_frame("categories")  # Changed to categories
        )
        offline.pack(pady=5)
        
        return_btn = ctk.CTkButton(
            self,
            text="Return",
            fg_color="red",
            command=lambda: parent.show_frame("welcome")
        )
        return_btn.pack(pady=40)
        

class QuizFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        
        self.parent = parent
        self.answer_var = ctk.StringVar()
        
        # Bigger font for question
        test = self.parent.questions[0]["question"]
        title = ctk.CTkLabel(
            self,
            text=test,
            text_color="white",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(50, 30))
        
        # Create options frame for better alignment
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.pack(pady=10)
        
        question = self.parent.questions[self.parent.current_question]
        
        # Add options with more spacing to the left
        for i, option in enumerate(question["options"], 1):
            ctk.CTkRadioButton(
                options_frame,
                text=option,
                variable=self.answer_var,
                value=str(i),
                text_color="white",
                font=("Arial", 14)
            ).pack(pady=10, padx=(50, 0), anchor="w")  # Left alignment with padding
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=40)  # Increased spacing between buttons
        
        ctk.CTkButton(
            btn_frame,
            text="Return",
            fg_color="red",
            command=lambda: parent.show_frame("mode")
        ).pack(side="left", padx=20)  # Increased spacing between buttons
        
        ctk.CTkButton(
            btn_frame,
            text="Next",
            fg_color="green",
            command=self.check_answer
        ).pack(side="left", padx=20)  # Increased spacing between buttons

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
            text="YOUR ANSWER WAS WRONG!!",
            text_color="red",
            font=("Arial", 24, "bold")
        ).pack(pady=(100, 20))
        
        ctk.CTkLabel(
            self,
            text="The right answer is:",
            text_color="white",
            font=("Arial", 16)
        ).pack(pady=5)
        
        question = parent.questions[parent.current_question]
        correct_answer = question["options"][int(question["correct"]) - 1]
        
        # Highlight the correct answer in green
        ctk.CTkLabel(
            self,
            text=correct_answer,
            text_color="#4CAF50",  # Green color for correct answer
            font=("Arial", 18, "bold")
        ).pack(pady=10)
        
        ctk.CTkButton(
            self,
            text="Next",
            fg_color="green",
            command=lambda: parent.show_frame("quiz")
        ).pack(pady=40)

class ScoreFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        
        ctk.CTkLabel(
            self,
            text=f"Your final score: {parent.score}/{len(parent.questions)}",
            text_color="white",
            font=("Arial", 24)
        ).pack(pady=(150, 20))
        
        ctk.CTkButton(
            self,
            text="Next",
            fg_color="green",
            command=self.save_and_return
        ).pack(pady=40)
    
    def save_and_return(self):
        with open('users.json', 'r') as f:
            users = json.load(f)
        
        users[self.master.current_user].append({
            'date': datetime.now().strftime('%d/%m/%Y'),
            'score': f"{self.master.score}/{len(self.master.questions)}"
        })
        
        with open('users.json', 'w') as f:
            json.dump(users, f)
        
        self.master.show_frame("history")

class HistoryFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        
        ctk.CTkLabel(
            self,
            text=f"History of\n{parent.current_user}:",
            text_color="white",
            font=("Arial", 20)
        ).pack(pady=(100, 20))
        
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
                history = users[parent.current_user]
                
                for entry in history[-3:]:
                    ctk.CTkLabel(
                        self,
                        text=f"date: {entry['date']}, score: {entry['score']}",
                        text_color="white",
                        font=("Arial", 14)
                    ).pack(pady=10)
        except:
            pass
        
        ctk.CTkButton(
            self,
            text="Next",
            fg_color="green",
            command=lambda: parent.show_frame("mode")
        ).pack(pady=40)

if __name__ == "__main__":
    app = MCQApp()
    app.mainloop()