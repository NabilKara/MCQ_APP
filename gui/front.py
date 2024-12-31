from doctest import master

import bcrypt
import customtkinter as ctk
import json
from datetime import datetime
import os
# import ...backend.user_management as user_management

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
            "start": StartFrame,
            "login": LoginFrame,
            "signup": SignupFrame,
            "welcome": WelcomeFrame,
            "mode": ModeFrame,
            "categories": CategoryFrame,
            "history": HistoryFrame,
            "quiz": QuizFrame,
            "wrong": WrongFrame,
            "score": ScoreFrame
        }

        self.current_frame = None
        self.show_frame("start")

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

class StartFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")

        # App Title
        ctk.CTkLabel(
            self,
            text="MCQ Quiz App",
            text_color="white",
            font=("Arial", 28, "bold")
        ).pack(pady=(80, 40))

        # Buttons Container
        btn_container = ctk.CTkFrame(self, fg_color="transparent")
        btn_container.pack(pady=20)

        # Login Button
        ctk.CTkButton(
            btn_container,
            text="Login",
            command=lambda: parent.show_frame("login"),
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=200,
            height=40,
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Signup Button
        ctk.CTkButton(
            btn_container,
            text="Sign Up",
            command=lambda: parent.show_frame("signup"),
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=200,
            height=40,
            font=("Arial", 16, "bold")
        ).pack(pady=10)

class SignupFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")

        # Greeting Label
        greeting = ctk.CTkLabel(
            self,
            text="Welcome to the MCQ Quiz App!",
            text_color="white",
            font=("Arial", 24, "bold")
        )
        greeting.pack(pady=(40, 20))

        # Login Container
        login_container = ctk.CTkFrame(self, fg_color="#3949ab", corner_radius=15)
        login_container.pack(pady=20, padx=40)

        # Username Entry
        self.username_entry = ctk.CTkEntry(
            login_container,
            placeholder_text="Enter username",
            width=280,
            fg_color="white",
            text_color="black",
            font=("Arial", 14)
        )
        self.username_entry.pack(pady=(20, 10), padx=20)
        self.username_entry.bind('<Return>', lambda e: self.check_user())  # Allow pressing Enter

        # Password Entry
        self.password_entry = ctk.CTkEntry(
            login_container,
            placeholder_text="Enter password",
            width=280,
            fg_color="white",
            text_color="black",
            font=("Arial", 14),
            show="*"  # Masks input characters with "*"
        )
        self.password_entry.pack(pady=(10, 10), padx=20)

        # Allow pressing Enter to trigger checkuser with both username and password
        self.password_entry.bind('<Return>', lambda e: self.check_user())

        # Login Button
        self.login_button = ctk.CTkButton(
            login_container,
            text="Sign Up",
            command=self.check_user,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            corner_radius=8
        )
        self.login_button.pack(pady=(10, 20))

        # Feedback Label
        self.feedback_label = ctk.CTkLabel(
            self,
            text="",
            text_color="yellow",
            font=("Arial", 14)
        )
        self.feedback_label.pack(pady=(10, 0))

    # This function will signup the user if it doesn't already exit
    def check_user(self):
        username = self.username_entry.get().strip()
        if not username:
            self.display_feedback("⚠️ Please enter a username.", "yellow")
            return

        password = self.password_entry.get().strip()
        if not password:
            self.display_feedback("⚠️ Please enter a password.", "yellow")
            return

        try:
            with open('data/users.json', 'r') as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.display_feedback("⚠️" + e.msg, "yellow")
            return

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        for user in users:
            if user == username and bcrypt.checkpw(password.encode(), hashed_password.encode()):
                self.display_feedback("⚠️ User already exists!.", "yellow")
                return
        new_user = {
            username: {
                "password": hashed_password,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "history": []
            },
        }

        users.update(new_user)
        with open('data/users.json', 'w') as file:
            json.dump(users, file, indent=4)

        # Set the current user and navigate to the next frame
        self.master.current_user = username
        self.master.current_userdata = new_user[username]
        self.master.show_frame("mode" if not users[username] else "welcome")

    def display_feedback(self, message, color):
        """
        Display feedback message to the user in the feedback label.
        The message disappears after a short delay.
        """
        self.feedback_label.configure(text=message, text_color=color)
        self.after(3000, lambda: self.feedback_label.configure(text=""))  # Clear the feedback after 3 seconds

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")

        # Greeting Label
        greeting = ctk.CTkLabel(
            self,
            text="Welcome to the MCQ Quiz App!",
            text_color="white",
            font=("Arial", 24, "bold")
        )
        greeting.pack(pady=(40, 20))

        # Login Container
        login_container = ctk.CTkFrame(self, fg_color="#3949ab", corner_radius=15)
        login_container.pack(pady=20, padx=40)

        # Username Entry
        self.username_entry = ctk.CTkEntry(
            login_container,
            placeholder_text="Enter username",
            width=280,
            fg_color="white",
            text_color="black",
            font=("Arial", 14)
        )
        self.username_entry.pack(pady=(20, 10), padx=20)
        self.username_entry.bind('<Return>', lambda e: self.check_user())  # Allow pressing Enter

        # Password Entry
        self.password_entry = ctk.CTkEntry(
            login_container,
            placeholder_text="Enter password",
            width=280,
            fg_color="white",
            text_color="black",
            font=("Arial", 14),
            show="*"  # Masks input characters with "*"
        )
        self.password_entry.pack(pady=(10, 10), padx=20)

        # Allow pressing Enter to trigger checkuser with both username and password
        self.password_entry.bind('<Return>', lambda e: self.check_user())

        # Login Button
        self.login_button = ctk.CTkButton(
            login_container,
            text="Login",
            command=self.check_user,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            corner_radius=8
        )
        self.login_button.pack(pady=(10, 20))

        # Feedback Label
        self.feedback_label = ctk.CTkLabel(
            self,
            text="",
            text_color="yellow",
            font=("Arial", 14)
        )
        self.feedback_label.pack(pady=(10, 0))

    def check_user(self):
        username = self.username_entry.get().strip()
        if not username:
            self.display_feedback("⚠️ Please enter a username.", "yellow")
            return

        password = self.password_entry.get().strip()
        if not password:
            self.display_feedback("⚠️ Please enter a password.", "yellow")
            return

        # Load user data
        try:
            with open('data/users.json', 'r') as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.display_feedback("⚠️" + e.msg, "yellow")
            return

        for user in users:
            if user == username and bcrypt.checkpw(password.encode(), users[user]["password"].encode()):
                self.master.current_user = username
                self.master.current_userdata = users[user]
                self.master.show_frame("mode" if not users[username] else "welcome")
                return

        # If user doesn't exist, notify and create a new user
        self.display_feedback(f"👤 User '{username}' does not exist!", "red")
        return

    def display_feedback(self, message, color):
        """
        Display feedback message to the user in the feedback label.
        The message disappears after a short delay.
        """
        self.feedback_label.configure(text=message, text_color=color)
        self.after(3000, lambda: self.feedback_label.configure(text=""))  # Clear the feedback after 3 seconds

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

        # Spacer to push content above
        spacer = ctk.CTkLabel(self, text="")
        spacer.pack(expand=True)  # Expand fills the available vertical space

        # Create a frame for the buttons
        button_container = ctk.CTkFrame(self, fg_color="transparent")
        button_container.pack(side="bottom", pady=20)  # Place at the bottom with padding

        # Button to view history
        ctk.CTkButton(
            button_container,
            text="Display History",
            fg_color="#FF9800",
            font=("Arial", 14),
            command=lambda: parent.show_frame("history")
        ).pack(side="left", padx=10)

        # Button to start a new quiz
        ctk.CTkButton(
            button_container,
            text="Start Quiz",
            fg_color="green",
            font=("Arial", 14),
            command=lambda: parent.show_frame("mode")
        ).pack(side="left", padx=10)

        # Button to log out and return to login screen
        ctk.CTkButton(
            button_container,
            text="Log out",
            fg_color="red",
            font=("Arial", 14),
            command=lambda: parent.show_frame("start")
        ).pack(side="left", padx=10)

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

import customtkinter as ctk

class QuizFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")

        # Configure frame size
        self.configure(width=600, height=400)
        self.pack_propagate(False)

        self.parent = parent
        self.answer_var = ctk.StringVar()

        # Handle case when no questions are available
        if not parent.questions:
            ctk.CTkLabel(
                self,
                text="No questions available",
                text_color="yellow",
                font=("Arial", 18)
            ).pack(pady=50)
            return

        # Create main container for content
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Display current question
        question = parent.questions[parent.current_question]

        # Question title
        title = ctk.CTkLabel(
            content_frame,
            text=question["question"],
            text_color="white",
            font=("Arial", 18, "bold"),
            wraplength=500  # Ensure long questions wrap properly
        )
        title.pack(pady=(20, 30))

        # Options frame
        options_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        options_frame.pack(pady=10, expand=True)

        # Create radio buttons for options
        for i, option in enumerate(question["options"], 1):
            option_btn = ctk.CTkRadioButton(
                options_frame,
                text=option,
                variable=self.answer_var,
                value=str(i),
                text_color="white",
                font=("Arial", 14),
                hover_color="#4a5fc1",  # Slightly lighter than background for hover effect
                fg_color="#2196f3",     # Material design blue
            )
            option_btn.pack(pady=10, padx=(50, 0), anchor="w")

        # Button frame at the bottom
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="bottom", pady=(0, 20), fill="x", padx=20)

        # Center the buttons using a container frame
        button_container = ctk.CTkFrame(btn_frame, fg_color="transparent")
        button_container.pack(expand=True)

        # Submit button
        ctk.CTkButton(
            button_container,
            text="Submit Answer",
            fg_color="#4caf50",  # Material design green
            hover_color="#388e3c",
            font=("Arial", 14, "bold"),
            width=150,
            height=40,
            corner_radius=8,
            command=self.check_answer
        ).pack(side="left", padx=10)

        # Quit button
        ctk.CTkButton(
            button_container,
            text="Quit Quiz",
            fg_color="#f44336",  # Material design red
            hover_color="#d32f2f",
            font=("Arial", 14, "bold"),
            width=150,
            height=40,
            corner_radius=8,
            command=lambda: parent.show_frame("mode")
        ).pack(side="left", padx=10)

        # Progress indicator
        progress_text = f"Question {parent.current_question + 1} of {len(parent.questions)}"
        progress_label = ctk.CTkLabel(
            self,
            text=progress_text,
            text_color="Green",
            font=("Arial", 12)
        )
        progress_label.pack(side="bottom", pady=(0, 5))

    def check_answer(self):
        """Verify the selected answer and handle the response"""
        # Ensure an answer is selected
        if not self.answer_var.get():
            self.show_error("Please select an answer")
            return

        question = self.parent.questions[self.parent.current_question]
        if self.answer_var.get() == question["correct"]:
            self.parent.score += 1
            self.next_question()
        else:
            self.parent.show_frame("wrong")

    def next_question(self):
        """Advance to the next question or show final score"""
        self.parent.current_question += 1
        if self.parent.current_question >= len(self.parent.questions):
            self.parent.show_frame("score")
        else:
            self.parent.show_frame("quiz")

    def show_error(self, message):
        """Display an error message to the user"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("300x150")
        error_window.transient(self)  # Make the window modal

        ctk.CTkLabel(
            error_window,
            text=message,
            font=("Arial", 14),
            text_color="white"
        ).pack(pady=20)

        ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy,
            width=100
        ).pack(pady=10)

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

        # Top navigation frame
        top_nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_nav_frame.pack(fill="x", padx=20, pady=(10, 0))

        # Return button
        ctk.CTkButton(
            top_nav_frame,
            text="← Return",
            fg_color="#2196F3",
            hover_color="#1976D2",
            font=("Arial", 14),
            width=100,
            command=lambda: parent.show_frame("welcome")
        ).pack(side="left")

        # Title
        ctk.CTkLabel(
            self,
            text=f"Quiz History for {parent.current_user}",
            text_color="white",
            font=("Arial", 24, "bold")
        ).pack(pady=(10, 20))

        # Create scrollable frame for history entries
        history_container = ctk.CTkScrollableFrame(
            self,
            width=500,
            height=300,
            fg_color="transparent"
        )
        history_container.pack(pady=20, padx=20, fill="both", expand=True)

        # Load and display history
        try:
            with open('data/users.json', 'r') as f:
                users = json.load(f)
                user_data = users.get(parent.current_user, {})
                history = user_data.get('history', [])

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

                        # Total Score
                        ctk.CTkLabel(
                            entry_frame,
                            text=f"Total Score: {entry['total_score']}",
                            text_color="#4CAF50",
                            font=("Arial", 14, "bold")
                        ).pack(pady=(0, 5), padx=10, anchor="w")

                        # Categories with individual scores
                        if 'categories' in entry:
                            categories_frame = ctk.CTkFrame(
                                entry_frame,
                                fg_color="transparent"
                            )
                            categories_frame.pack(pady=(0, 5), padx=10, fill="x")

                            ctk.CTkLabel(
                                categories_frame,
                                text="Category Scores:",
                                text_color="white",
                                font=("Arial", 12, "bold")
                            ).pack(anchor="w")

                            for category_entry in entry['categories']:
                                category_text = f"{category_entry['category']}: {category_entry['score']}"
                                ctk.CTkLabel(
                                    categories_frame,
                                    text=category_text,
                                    text_color="white",
                                    font=("Arial", 12)
                                ).pack(pady=(0, 2), anchor="w")

        except Exception as e:
            ctk.CTkLabel(
                history_container,
                text="Error loading history",
                text_color="red",
                font=("Arial", 16)
            ).pack(pady=20)
            print(f"Error loading history: {e}")

        # Add buttons at the bottom
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(20, 10), padx=20, fill="x", side="bottom")

        # Buttons
        ctk.CTkButton(
            btn_frame,
            text="New Quiz",
            fg_color="green",
            font=("Arial", 14),
            command=lambda: parent.show_frame("mode")
        ).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Return to Welcome",
            fg_color="#FF9800",
            font=("Arial", 14),
            command=lambda: parent.show_frame("welcome")
        ).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Logout",
            fg_color="red",
            font=("Arial", 14),
            command=lambda: parent.show_frame("login")
        ).pack(side="left", padx=10, pady=10)


    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")

        # Add return button at the top
        top_btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_btn_frame.pack(pady=(10, 0), padx=20, anchor="w")

        ctk.CTkButton(
            top_btn_frame,
            text="← Return",
            fg_color="#FF9800",
            hover_color="#F57C00",
            font=("Arial", 14),
            command=lambda: parent.show_frame("welcome"),
            width=100,
            height=32
        ).pack(side="left")

        # Title
        ctk.CTkLabel(
            self,
            text=f"Quiz History for {parent.current_user}",
            text_color="white",
            font=("Arial", 24, "bold")
        ).pack(pady=(10, 20))

        # Create scrollable frame for history entries
        history_container = ctk.CTkScrollableFrame(
            self,
            width=500,
            height=300,
            fg_color="transparent"
        )
        history_container.pack(pady=20, padx=20, fill="both", expand=True)

        # Load and display history
        try:
            with open('data/users.json', 'r') as f:
                users = json.load(f)
                user_data = users.get(parent.current_user, {})
                
                if not user_data or 'history' not in user_data:
                    ctk.CTkLabel(
                        history_container,
                        text="No quiz history available",
                        text_color="yellow",
                        font=("Arial", 16)
                    ).pack(pady=20)
                else:
                    history = user_data['history']
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
                            text=f"Date: {entry.get('date', 'N/A')}",
                            text_color="white",
                            font=("Arial", 14)
                        ).pack(pady=(5, 0), padx=10, anchor="w")

                        # Total Score
                        total_score = entry.get('total_score', 'N/A')
                        ctk.CTkLabel(
                            entry_frame,
                            text=f"Total Score: {total_score}",
                            text_color="#4CAF50",
                            font=("Arial", 14, "bold")
                        ).pack(pady=(0, 5), padx=10, anchor="w")

                        # Categories and their scores
                        if 'categories' in entry:
                            categories_frame = ctk.CTkFrame(
                                entry_frame,
                                fg_color="transparent"
                            )
                            categories_frame.pack(pady=(0, 5), padx=10, fill="x")
                            
                            for category_data in entry['categories']:
                                category = category_data.get('category', 'Unknown')
                                score = category_data.get('score', 'N/A')
                                category_text = f"{category}: {score}"
                                
                                ctk.CTkLabel(
                                    categories_frame,
                                    text=category_text,
                                    text_color="white",
                                    font=("Arial", 12)
                                ).pack(pady=(0, 2), padx=10, anchor="w")

        except Exception as e:
            error_msg = ctk.CTkLabel(
                history_container,
                text=f"Error loading history: {str(e)}",
                text_color="red",
                font=("Arial", 16)
            )
            error_msg.pack(pady=20)
            print(f"Error loading history: {e}")

        # Navigation buttons frame
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(20, 10), padx=20, fill="x", side="bottom")

        # Navigation buttons
        ctk.CTkButton(
            btn_frame,
            text="New Quiz",
            fg_color="green",
            font=("Arial", 14),
            command=lambda: parent.show_frame("mode")
        ).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Return to Welcome",
            fg_color="#FF9800",
            font=("Arial", 14),
            command=lambda: parent.show_frame("welcome")
        ).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Logout",
            fg_color="red",
            font=("Arial", 14),
            command=lambda: parent.show_frame("login")
        ).pack(side="left", padx=10, pady=10)

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
            height=300,
            fg_color="transparent"
        )
        history_container.pack(pady=20, padx=20, fill="both", expand=True)

        # Load and display history
        try:
            with open('data/users.json', 'r') as f:
                users = json.load(f)
                user_data = users.get(parent.current_user, {})
                history = user_data.get('history', [])

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

                        # Total Score
                        ctk.CTkLabel(
                            entry_frame,
                            text=f"Total Score: {entry['total_score']}",
                            text_color="#4CAF50",
                            font=("Arial", 14, "bold")
                        ).pack(pady=(0, 5), padx=10, anchor="w")

                        # Categories with individual scores
                        if 'categories' in entry:
                            categories_frame = ctk.CTkFrame(
                                entry_frame,
                                fg_color="transparent"
                            )
                            categories_frame.pack(pady=(0, 5), padx=10, fill="x")

                            ctk.CTkLabel(
                                categories_frame,
                                text="Category Scores:",
                                text_color="white",
                                font=("Arial", 12, "bold")
                            ).pack(anchor="w")

                            for category_entry in entry['categories']:
                                category_text = f"{category_entry['category']}: {category_entry['score']}"
                                ctk.CTkLabel(
                                    categories_frame,
                                    text=category_text,
                                    text_color="white",
                                    font=("Arial", 12)
                                ).pack(pady=(0, 2), anchor="w")

        except Exception as e:
            ctk.CTkLabel(
                history_container,
                text="Error loading history",
                text_color="red",
                font=("Arial", 16)
            ).pack(pady=20)
            print(f"Error loading history: {e}")

        # Add buttons at the bottom
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(20, 10), padx=20, fill="x", side="bottom")

        # Buttons
        ctk.CTkButton(
            btn_frame,
            text="New Quiz",
            fg_color="green",
            font=("Arial", 14),
            command=lambda: parent.show_frame("mode")
        ).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Return to Welcome",
            fg_color="#FF9800",
            font=("Arial", 14),
            command=lambda: parent.show_frame("welcome")
        ).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Logout",
            fg_color="red",
            font=("Arial", 14),
            command=lambda: parent.show_frame("login")
        ).pack(side="left", padx=10, pady=10)

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
            with open('data/users.json', 'r') as f:
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
            with open('data/users.json', 'w') as f:
                json.dump(users, f, indent=4)

        except Exception as e:
            print(f"Error saving score: {e}")

if __name__ == "__main__":
    app = MCQApp()
    app.mainloop()