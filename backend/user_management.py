import json
import bcrypt
from datetime import datetime
import os

def ensure_data_directory():
    os.makedirs('data', exist_ok=True)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "User already exists"
        
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = {
        "password": hashed_password,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "history": []
    }
    
    save_users(users)
    return True, users[username]
    
def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found"
        
    if bcrypt.checkpw(password.encode(), users[username]["password"].encode()):
        return True, users[username]
    return False, "Invalid password"
    
def save_quiz_result(username, score, total_questions, categories):
    users = load_users()
    if username not in users:
        return False
        
    score_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_score": f"{score}/{total_questions}",
        "categories": [{"category": cat, "score": score} for cat in categories]
    }
    
    users[username]["history"].append(score_entry)
    save_users(users)
    return True
    
def load_users():
    try:
        with open('data/users.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
        
def save_users(users):
    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=4)

def save_score(parent):
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
def check_user_login(self):
        username = self.username_entry.get().strip()
        if not username:
            display_feedback(self,"⚠️ Please enter a username.", "yellow")
            return

        password = self.password_entry.get().strip()
        if not password:
            display_feedback(self,"⚠️ Please enter a password.", "yellow")
            return

        # Load user data
        try:
            with open('data/users.json', 'r') as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            display_feedback(self,"⚠️" + e.msg, "yellow")
            return

        for user in users:
            if user == username and bcrypt.checkpw(password.encode(), users[user]["password"].encode()):
                self.master.current_user = username
                self.master.current_userdata = users[user]
                self.master.show_frame("mode" if not users[username] else "welcome")
                return
            
        display_feedback(f"👤 Wrong username or password", "red")
        return

def check_user_singup(self):
        username = self.username_entry.get().strip()
        if not username:
            display_feedback(self,"⚠️ Please enter a username.", "yellow")
            return

        password = self.password_entry.get().strip()
        if not password:
            display_feedback(self,"⚠️ Please enter a password.", "yellow")
            return

        try:
            with open('data/users.json', 'r') as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            display_feedback(self,"⚠️" + e.msg, "yellow")
            return

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        for user in users:
            if user == username and bcrypt.checkpw(password.encode(), hashed_password.encode()):
                display_feedback(self,"⚠️ User already exists!.", "yellow")
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

        self.master.current_user = username
        self.master.current_userdata = new_user[username]
        self.master.show_frame("mode" if not users[username] else "welcome")

def display_feedback(self, message, color):
    self.feedback_label.configure(text=message, text_color=color)
    self.after(3000, lambda: self.feedback_label.configure(text=""))