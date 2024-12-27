import customtkinter as ctk
import json
from datetime import datetime

class MCQApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MCQ Quiz App")
        self.geometry("600x400")
        
        # Set dark blue theme
        self.configure(fg_color="#1a237e")  # Dark blue background
        
        self.current_user = None
        self.score = 0
        self.current_question = 0
        
        # Sample offline questions
        self.questions = [
            {
                "question": "What is Python?",
                "options": ["A snake", "A programming language", "A bird", "A food"],
                "correct": "2"
            },
            
            # Add more questions as needed
        ]
        
        self.frames = {
            "login": LoginFrame,
            "mode": ModeFrame,
            "history": HistoryFrame,
            "quiz": QuizFrame,
            "wrong": WrongFrame,
            "score": ScoreFrame
        }
        
        self.current_frame = None
        self.show_frame("login")
    
    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.destroy()
        
        Frame = self.frames[frame_name]
        self.current_frame = Frame(self)
        self.current_frame.pack(fill="both", expand=True)

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1a237e")
        
        self.username_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter username",
            width=200,
            fg_color="gray70"
        )
        self.username_entry.pack(pady=(150, 0))
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
        self.master.show_frame("mode")

class ModeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1a237e")
        
        title = ctk.CTkLabel(self, text="Choose the mode:", text_color="white")
        title.pack(pady=(100, 20))
        
        self.mode_var = ctk.StringVar()
        
        online = ctk.CTkRadioButton(
            self,
            text="online mode",
            variable=self.mode_var,
            value="online",
            text_color="white"
        )
        online.pack(pady=5)
        
        offline = ctk.CTkRadioButton(
            self,
            text="offline mode",
            variable=self.mode_var,
            value="offline",
            text_color="white",
            command=lambda: parent.show_frame("quiz")
        )
        offline.pack(pady=5)
        
        return_btn = ctk.CTkButton(
            self,
            text="Return",
            fg_color="red",
            command=lambda: parent.show_frame("login")
        )
        return_btn.pack(pady=20)

class QuizFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1a237e")
        
        self.parent = parent
        self.answer_var = ctk.StringVar()
        test = self.parent.questions[0]["question"]
        title = ctk.CTkLabel(
            self,
            text=test,
            text_color="white"
        )
        title.pack(pady=(50, 20))
        
        question = self.parent.questions[self.parent.current_question]
        
        for i, option in enumerate(question["options"], 1):
            ctk.CTkRadioButton(
                self,
                text=option,
                variable=self.answer_var,
                value=str(i),
                text_color="white"
            ).pack(pady=5)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Return",
            fg_color="red",
            command=lambda: parent.show_frame("mode")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Next",
            fg_color="green",
            command=self.check_answer
        ).pack(side="left", padx=5)

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
        super().__init__(parent, fg_color="#1a237e")
        
        ctk.CTkLabel(
            self,
            text="YOUR ANSWER WAS WRONG!!",
            text_color="red",
            font=("Arial", 20, "bold")
        ).pack(pady=(100, 20))
        
        ctk.CTkLabel(
            self,
            text="The right answer is:",
            text_color="white"
        ).pack(pady=5)
        
        question = parent.questions[parent.current_question]
        correct_answer = question["options"][int(question["correct"]) - 1]
        
        ctk.CTkLabel(
            self,
            text=correct_answer,
            text_color="white"
        ).pack(pady=1)
        
        ctk.CTkButton(
            self,
            text="Next",
            fg_color="green",
            command=lambda: parent.show_frame("quiz")
        ).pack(pady=20,padx=5)

class ScoreFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1a237e")
        
        ctk.CTkLabel(
            self,
            text=f"Your final score: {parent.score}/{len(parent.questions)}",
            text_color="white",
            font=("Arial", 20)
        ).pack(pady=(150, 20))
        
        ctk.CTkButton(
            self,
            text="Next",
            fg_color="green",
            command=self.save_and_return
        ).pack(pady=20,padx=5)
    
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
        super().__init__(parent, fg_color="#1a237e")
        
        ctk.CTkLabel(
            self,
            text=f"History of\n{parent.current_user}:",
            text_color="white"
        ).pack(pady=(100, 20))
        
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
                history = users[parent.current_user]
                
                for entry in history[-3:]:
                    ctk.CTkLabel(
                        self,
                        text=f"date: {entry['date']}, score: {entry['score']}",
                        text_color="white"
                    ).pack(pady=5)
        except:
            pass
        
        ctk.CTkButton(
            self,
            text="Next",
            fg_color="green",
            command=lambda: parent.show_frame("mode")
        ).pack(pady=20,padx=5)

if __name__ == "__main__":
    app = MCQApp()
    app.mainloop()