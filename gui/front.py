import json
import customtkinter as ctk
import backend.question_management as qm
import backend.score_evaluation as se
import backend.user_management as um

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

        um.ensure_data_directory()

        self.all_questions = qm.load_questions()

        self.frames = {
            "start": StartFrame,
            "login": LoginFrame,
            "signup": SignupFrame,
            "welcome": WelcomeFrame,
            "mode": ModeFrame,
            "categories": CategoryFrame,
            "history": HistoryFrame,
            "quiz": QuizFrame,
            "correct": CorrectFrame,
            "wrong": WrongFrame,
            "score": ScoreFrame
        }

        self.current_frame = None
        self.show_frame("start")

    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.destroy()

        Frame = self.frames[frame_name]
        self.current_frame = Frame(self)
        self.current_frame.pack(fill="both", expand=True)

    def prepare_quiz(self):
        """Prepare quiz questions based on selected categories."""
        self.questions = []
        self.score = []  # Initialize the score array

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
        self.current_question = 0

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

        greeting = ctk.CTkLabel(
            self,
            text="Welcome to the MCQ Quiz App!",
            text_color="white",
            font=("Arial", 24, "bold")
        )
        greeting.pack(pady=(40, 20))

        login_container = ctk.CTkFrame(self, fg_color="#3949ab", corner_radius=15)
        login_container.pack(pady=20, padx=40)

        self.username_entry = ctk.CTkEntry(
            login_container,
            placeholder_text="Enter username",
            width=280,
            fg_color="white",
            text_color="black",
            font=("Arial", 14)
        )
        self.feedback_label = ctk.CTkLabel(
            self,
            text="",
            text_color="yellow",
            font=("Arial", 14)
        )

        self.username_entry.pack(pady=(20, 10), padx=20)
        self.username_entry.bind('<Return>', lambda e: um.check_user_singup(self))

        self.password_entry = ctk.CTkEntry(
            login_container,
            placeholder_text="Enter password",
            width=280,
            fg_color="white",
            text_color="black",
            font=("Arial", 14),
            show="*"
        )
        self.password_entry.pack(pady=(10, 10), padx=20)
        self.password_entry.bind('<Return>', lambda e: um.check_user_singup(self))

        button_container = ctk.CTkFrame(login_container, fg_color="transparent")
        button_container.pack(pady=(10, 20))

        self.signup_button = ctk.CTkButton(
            button_container,
            text="Sign Up",
            command= lambda: um.check_user_singup(self),
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            corner_radius=8
        )
        self.signup_button.pack(side="left", padx=10)

        self.return_button = ctk.CTkButton(
            button_container,
            text="Return",
            command=lambda: self.master.show_frame("start"),
            fg_color="#f44336",
            hover_color="#d32f2f",
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            corner_radius=8
        )
        self.return_button.pack(side="left", padx=10)

        
        self.feedback_label.pack(pady=(10, 0))

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

        # Feedback Label
        self.feedback_label = ctk.CTkLabel(
            self,
            text="",
            text_color="yellow",
            font=("Arial", 14)
        )

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
        self.username_entry.bind('<Return>', lambda e: um.check_user_login(self))

        # Password Entry
        self.password_entry = ctk.CTkEntry(
            login_container,
            placeholder_text="Enter password",
            width=280,
            fg_color="white",
            text_color="black",
            font=("Arial", 14),
            show="*"
        )
        self.password_entry.pack(pady=(10, 10), padx=20)
        self.password_entry.bind('<Return>', lambda e: um.check_user_login(self))

        # Button Container
        button_container = ctk.CTkFrame(login_container, fg_color="transparent")
        button_container.pack(pady=(10, 20))

        # Login Button
        self.login_button = ctk.CTkButton(
            button_container,
            text="Login",
            command=lambda: um.check_user_login(self),
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            corner_radius=8
        )
        self.login_button.pack(side="left", padx=10)

        # Return Button
        self.return_button = ctk.CTkButton(
            button_container,
            text="Return",
            command=lambda: self.master.show_frame("start"),
            fg_color="#f44336",
            hover_color="#d32f2f",
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            corner_radius=8
        )
        self.return_button.pack(side="left", padx=10)

        
        self.feedback_label.pack(pady=(10, 0))
        return

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

class QuizFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")
        self.configure(width=600, height=400)
        self.pack_propagate(False)
        
        self.parent = parent
        self.answer_var = ctk.StringVar()

        if not parent.questions:
            ctk.CTkLabel(self, text="No questions available", text_color="yellow", font=("Arial", 18)).pack(pady=50)
            return

        # Progress bar
        progress_frame = ctk.CTkFrame(self, fg_color="#2196f3", height=40)
        progress_frame.pack(fill="x")
        progress_frame.pack_propagate(False)
        
        progress_text = f"Question {parent.current_question + 1} of {len(parent.questions)}"
        progress_label = ctk.CTkLabel(progress_frame, text=progress_text, text_color="white", font=("Arial", 16, "bold"))
        progress_label.pack(expand=True)

        # Question container
        question_container = ctk.CTkFrame(self, fg_color="transparent")
        question_container.pack(expand=True, fill="both", padx=20, pady=(10, 20))

        question = parent.questions[parent.current_question]
        
        # Question title - centered
        title = ctk.CTkLabel(
            question_container, 
            text=question["question"], 
            text_color="white", 
            font=("Arial", 18, "bold"), 
            wraplength=500,
            justify="center"
        )
        title.pack(expand=True, anchor="center", pady=(0, 20))

        # Options container - centered
        options_container = ctk.CTkFrame(question_container, fg_color="transparent")
        options_container.pack(expand=True, anchor="center", pady=(0, 20))

        for i, option in enumerate(question["options"], 1):
            option_btn = ctk.CTkRadioButton(
                options_container,
                text=option,
                variable=self.answer_var,
                value=str(i),
                text_color="white",
                font=("Arial", 14),
                hover_color="#4a5fc1",
                fg_color="#2196f3"
            )
            option_btn.pack(pady=10, anchor="w")

        # Button frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        button_frame.pack(fill="x", side="bottom")
        button_frame.pack_propagate(False)

        button_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        button_container.pack(expand=True)

        submit_btn = ctk.CTkButton(
            button_container,
            text="Submit Answer",
            command=self.check_answer,
            fg_color="#4caf50",
            hover_color="#388e3c",
            font=("Arial", 14, "bold"),
            width=150,
            height=40,
            corner_radius=8
        )
        submit_btn.pack(side="left", padx=10)

        quit_btn = ctk.CTkButton(
            button_container,
            text="Quit Quiz",
            command=lambda: parent.show_frame("mode"),
            fg_color="#f44336",
            hover_color="#d32f2f",
            font=("Arial", 14, "bold"),
            width=150,
            height=40,
            corner_radius=8
        )
        quit_btn.pack(side="left", padx=10)

    def check_answer(self):
        if not self.answer_var.get():
            self.show_error("Please select an answer")
            return

        parent = self.parent
        question = parent.questions[parent.current_question]

        for i, (cat, current_score, num_questions) in enumerate(parent.score):
            if cat == question["category"]:
                parent.score[i] = (cat, current_score, num_questions + 1)
                break

        if self.answer_var.get() == question["correct"]:
            for i, (cat, current_score, num_questions) in enumerate(parent.score):
                if cat == question["category"]:
                    parent.score[i] = (cat, current_score + 1, num_questions)
                    break
            # self.next_question()
            parent.show_frame("correct")
        else:
            parent.show_frame("wrong")

    def next_question(self):
        parent = self.parent
        parent.current_question += 1
        if parent.current_question >= len(parent.questions):
            parent.show_frame("score")
        else:
            parent.show_frame("quiz")

    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("300x150")
        error_window.transient(self)

        ctk.CTkLabel(error_window, text=message, font=("Arial", 14), text_color="white").pack(pady=20)
        ctk.CTkButton(error_window, text="OK", command=error_window.destroy, width=100).pack(pady=10)

class CorrectFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#4CAF50")  # Green background for correct answer

        ctk.CTkLabel(
            self,
            text="Correct!",
            text_color="white",
            font=("Arial", 24, "bold")
        ).pack(pady=(150, 20))  # Vertically centered

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

class ScoreFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3f51b5")

        # Calculate percentage score
        percentage = se.calculate_percentage(parent.score)
        # Display score
        ctk.CTkLabel(
            self,
            text="Quiz Complete!",
            text_color="white",
            font=("Arial", 24, "bold")
        ).pack(pady=(50, 20))

        ctk.CTkLabel(
            self,
            text=f"Your Score: {percentage}",
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
        performance_text = se.evaluate_performance(percentage)
        ctk.CTkLabel(
            self,
            text=performance_text,
            text_color="#4CAF50",
            font=("Arial", 18)
        ).pack(pady=20)

        # Save score to user history
        um.save_score(parent)

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