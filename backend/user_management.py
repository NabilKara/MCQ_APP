import json
from datetime import datetime
import bcrypt

def signup(username, password):
    try:
        with open('data/users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        return False, 'data/users.json file not found!'

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    for user in users:
        if user == username and bcrypt.checkpw(password.encode(), hashed_password.encode()):
            return False, 'User already exists!'

    new_user = {
        username: {
            "password": hashed_password,
            "created_at":  datetime.now().strftime("%Y-%m-%d %H:%M"),
            "history": []
        },
    }
    users.update(new_user)
    with open('data/users.json', 'w') as file:
        json.dump(users, file, indent=4)

    return True, new_user

def login(username, password):
    try:
        with open('data/users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        return False, 'data/users.json file not found!'

    for user in users:
        if user == username and bcrypt.checkpw(password.encode(), users[user]["password"].encode()):
            # self.master = user
            # return True
            return True, user, users[user]

    return False, 'Invalid username or password!'

# signup test
# result = signup("abdou5", "pass5")
# print(result)

# login test
# result = login("abdou3", "pass3")
# print(result)