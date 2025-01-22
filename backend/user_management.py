import json
import bcrypt
from datetime import datetime
import os
import csv

def ensure_data_directory():
    os.makedirs('data', exist_ok=True)

def load_users():
    """
    Load the user data from the JSON file. If the file does not exist or is empty, return an empty dictionary.
    """
    try:
        with open('data/users.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_score(parent):
    """
    Save the quiz score to the user's history field in the JSON file.
    """
    try:
        with open('data/users.json', 'r') as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error:", e)
        return

    nb_questions = 0
    total_score = 0

    for i, (cat, current_score, num_questions) in enumerate(parent.score):
        nb_questions += num_questions
        total_score += current_score

    # Create the new history entry
    history_entry = {
        "total_score": f"{total_score}/{nb_questions}",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "categories": [
            {"category": cat, "score": f"{current_score}/{num_questions}"}
            for i, (cat, current_score, num_questions) in enumerate(parent.score)
        ]
    }

    users[parent.current_user]["history"].append(history_entry)

    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=4)

def check_fields(self):
    """
    Check if the username and password fields in the login and signup frame are filled and return the values.
    """
    username = self.username_entry.get().strip()
    if not username:
        display_feedback(self, "⚠️ Please enter a username.", "yellow")
        return False

    password = self.password_entry.get().strip()
    if not password:
        display_feedback(self, "⚠️ Please enter a password.", "yellow")
        return False
    try:
        confirm_password = self.confirm_password_entry.get().strip()
        if not confirm_password:
            display_feedback(self, "⚠️ Please confirm your password.", "yellow")
            return False
        if password != confirm_password:
            display_feedback(self, "⚠️ Passwords do not match.", "yellow")
            return False
    except AttributeError:
        pass
    # Load user data
    try:
        with open('data/users.json', 'r') as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        display_feedback(self, "⚠️" + e.msg, "yellow")
        return False

    return True, username, password, users

def check_user_login(self):
    """
    Check if the user exists in the user data and if the password is correct. If so, log in the user.
    """
    result = check_fields(self)
    if not result:
        return
    username = result[1]
    password = result[2]
    users = result[3]

    for user in users:
        if user == username and bcrypt.checkpw(password.encode(), users[user]["password"].encode()):
            self.master.current_user = username
            self.master.current_userdata = users[user]
            self.master.show_frame("mode" if not users[username] else "welcome")
            return

    display_feedback(self, f"👤 Wrong username or password", "red")
    return

def check_user_singup(self):
    """
    Check if the user already exists in the user data. If not, create a new user."""
    result = check_fields(self)
    if not result:
        return
    username = result[1]
    password = result[2]
    users = result[3]

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

def export_csv(username, file_path=None):
    """
    Export the user's quiz history to a CSV file.
    """
    users = load_users()
    if username not in users.keys():
        return False, "User not found"
    
    # If no file path provided, create default in current directory
    if file_path is None:
        default_filename = f"{username}_{datetime.now().strftime('%Y-%m-%d-%H-%M')}.csv"
        file_path = os.path.join(os.getcwd(), default_filename)
    
    try:
        history = users[username]["history"]

        file = open(file_path, mode="w", newline="")
        writer = csv.writer(file)
        writer.writerow(["Date", "Total Score", "Category", "Category Score"])
        for entry in history:
            date = entry["date"]
            total_score = entry["total_score"]
            writer.writerows([[date, total_score, cat["category"], cat["score"]] for cat in entry["categories"]])

        return True, f"Successfully exported to {file_path}"
    
    except Exception as e:
        return False, f"Error exporting file: {str(e)}"
    
def display_feedback(self, message, color):
    """
    Display feedback message to the
    user on the main window.
    """
    self.feedback_label.configure(text=message, text_color=color)
    self.after(3000, lambda: self.feedback_label.configure(text=""))
