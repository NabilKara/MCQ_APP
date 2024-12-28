import customtkinter as ctk
import json


class MCQApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MCQ Quiz App")
        self.geometry("600x400")
        self.configure(fg_color="#1a237e")

        self.current_user = None
        self.score = 0
        self.current_question = 0
        self.selected_categories = []
        self.questions = []
        self.mode = None

        # Load questions from JSON file or fallback to default
        self.all_questions = self.load_questions()
        self.history = []

        # Frames
        self.frames = {
            "login": LoginFrame,
            "mode": ModeFrame,
            "category": CategoryFrame,
            "history": HistoryFrame,
            "quiz": QuizFrame,
            "wrong": WrongFrame,
            "score": ScoreFrame
        }

        self.current_frame = None
        self.show_frame("login")

    def load_questions(self):
        """Load questions from JSON file, or use defaults if the file is not found."""
        try:
            with open('data/questions.json', 'r') as f:
                print("File opening succeeded")
                return json.load(f)
        except FileNotFoundError:
            # Default questions if JSON file is missing
            return {
                "Python": [
                    {
                        "question": "What is Python?",
                        "options": ["Programming Language", "Snake", "Movie", "Game"],
                        "answer": "Programming Language"
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
                        "answer": "Central Processing Unit"
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
                        "answer": "Identifies a device on a network"
                    }
                ]
            }

    def show_frame(self, frame_name):
        """Display a specific frame."""
        if self.current_frame:
            self.current_frame.destroy()

        Frame = self.frames[frame_name]
        self.current_frame = Frame(self)
        self.current_frame.pack(fill="both", expand=True)

    def prepare_quiz(self):
        """Prepare quiz questions based on selected categories."""
        self.questions = []
        for category in self.selected_categories:
            print(category)
            self.questions.extend(self.all_questions.get(category, []))
        print(self.questions)
        self.current_question = 0
        self.score = 0

    def save_history(self):
        """Save the user's quiz history."""
        self.history.append({
            "user": self.current_user,
            "score": self.score,
            "total_questions": len(self.questions),
            "categories": self.selected_categories
        })


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1a237e")

        title = ctk.CTkLabel(self, text="Welcome to MCQ Quiz App", text_color="white", font=("Arial", 20))
        title.pack(pady=(50, 20))

        username_label = ctk.CTkLabel(self, text="Enter Username:", text_color="white")
        username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack()

        login_button = ctk.CTkButton(self, text="Login", command=self.login)
        login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        if username:
            self.master.current_user = username
            self.master.show_frame("mode")


class ModeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1a237e")

        title = ctk.CTkLabel(self, text="Choose Quiz Mode", text_color="white", font=("Arial", 20))
        title.pack(pady=(50, 20))

        offline_button = ctk.CTkButton(self, text="Offline Mode", command=lambda: self.set_mode("offline"))
        offline_button.pack(pady=10)

        online_button = ctk.CTkButton(self, text="Online Mode (Unavailable)", command=lambda: self.set_mode("online"))
        online_button.pack(pady=10)

    def set_mode(self, mode):
        self.master.mode = mode
        self.master.show_frame("category")


class CategoryFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1a237e")

        title = ctk.CTkLabel(
            self,
            text=f"Select Categories ({parent.mode.title()} Mode):",
            text_color="white",
            font=("Arial", 20),
            wraplength=500,
            anchor="center"
        )
        title.pack(pady=(50, 20))

        self.category_vars = {}
        categories = ["Python", "Computer Science", "Networking"]

        checkbox_frame = ctk.CTkFrame(self, fg_color="transparent")
        checkbox_frame.pack(pady=(20, 10))

        for category in categories:
            var = ctk.BooleanVar()
            self.category_vars[category] = var
            ctk.CTkCheckBox(
                checkbox_frame,
                text=category,
                variable=var,
                text_color="white"
            ).pack(anchor="w", padx=10, pady=5)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

        start_btn = ctk.CTkButton(
            btn_frame,
            text="Start Quiz",
            fg_color="green",
            command=self.start_quiz
        )
        start_btn.pack(side="left", padx=5)

        return_btn = ctk.CTkButton(
            btn_frame,
            text="Change Mode",
            fg_color="red",
            command=lambda: parent.show_frame("mode")
        )
        return_btn.pack(side="left", padx=5)

    def start_quiz(self):
        selected = [cat for cat, var in self.category_vars.items() if var.get()]
        if not selected:
            ctk.CTkLabel(
                self,
                text="Please select at least one category",
                text_color="yellow"
            ).pack(pady=10)
            return

        self.master.selected_categories = selected
        self.master.prepare_quiz()

        if self.master.mode == "online" and not self.master.questions:
            ctk.CTkLabel(
                self,
                text="Online mode is not available yet",
                text_color="yellow"
            ).pack(pady=10)
            return

        self.master.show_frame("quiz")


class QuizFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1a237e")

        if parent.questions:
            print("enter parent.questions")
            question = parent.questions[parent.current_question]["question"]
            print(question)
            options = parent.questions[parent.current_question]["options"]
            print(options)
            question_label = ctk.CTkLabel(self, text=question, text_color="white", wraplength=500)
            question_label.pack(pady=20)

            for option in options:
                ctk.CTkButton(self, text=option, command=lambda opt=option: self.check_answer(opt)).pack(pady=5)
        else:
            ctk.CTkLabel(self, text="No questions available.", text_color="yellow").pack(pady=20)

    def check_answer(self, selected_option):
        correct_answer = self.master.questions[self.master.current_question]["answer"]
        if selected_option == correct_answer:
            self.master.score += 1
        self.master.current_question += 1

        if self.master.current_question >= len(self.master.questions):
            self.master.save_history()
            self.master.show_frame("score")
        else:
            self.master.show_frame("quiz")


class ScoreFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1a237e")

        ctk.CTkLabel(self, text="Quiz Completed!", text_color="white", font=("Arial", 20)).pack(pady=20)
        ctk.CTkLabel(self, text=f"Your Score: {parent.score}/{len(parent.questions)}", text_color="yellow").pack(pady=10)

        restart_button = ctk.CTkButton(self, text="Restart", command=lambda: parent.show_frame("mode"))
        restart_button.pack(pady=20)

        history_button = ctk.CTkButton(self, text="View History", command=lambda: parent.show_frame("history"))
        history_button.pack(pady=10)


class HistoryFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1a237e")

        title = ctk.CTkLabel(self, text="Quiz History", text_color="white", font=("Arial", 20))
        title.pack(pady=20)

        if not parent.history:
            ctk.CTkLabel(self, text="No history available.", text_color="yellow").pack(pady=10)
        else:
            for record in parent.history:
                history_text = f"User: {record['user']}, Score: {record['score']}/{record['total_questions']}, Categories: {', '.join(record['categories'])}"
                ctk.CTkLabel(self, text=history_text, text_color="white").pack(pady=5)

        back_button = ctk.CTkButton(self, text="Back", command=lambda: parent.show_frame("score"))
        back_button.pack(pady=20)


class WrongFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1a237e")

        title = ctk.CTkLabel(self, text="Wrong Answers", text_color="white", font=("Arial", 20))
        title.pack(pady=20)

        wrong_answers = []
        for idx, question in enumerate(parent.questions):
            user_answer = question.get("user_answer")
            if user_answer != question["answer"]:
                wrong_answers.append(f"Q: {question['question']} - Your Answer: {user_answer} - Correct Answer: {question['answer']}")

        if wrong_answers:
            for answer in wrong_answers:
                ctk.CTkLabel(self, text=answer, text_color="yellow").pack(pady=5)
        else:
            ctk.CTkLabel(self, text="No wrong answers.", text_color="yellow").pack(pady=10)

        back_button = ctk.CTkButton(self, text="Back", command=lambda: parent.show_frame("score"))
        back_button.pack(pady=20)


if __name__ == "__main__":
    app = MCQApp()
    app.mainloop()