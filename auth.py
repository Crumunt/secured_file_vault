import json
import hashlib
import helper

def login(username, password):

    with open("users.json", "r") as f:
       users = json.load(f)

    found_user = 0

    for user in users:
        if user.get("username") == username:
            user_password = user.get("password")
            found_user = 1
            break
    
    if found_user == 0:
        return False

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    if hashed_password != user_password:
        helper.log_action("Incorrect username/password", username)
        return False
    

    helper.log_action("Login", username)
    return True


def register(username, password, confirm_password):
    if password != confirm_password or len(password) < 8:
        return False
    

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    new_user = {
        "username": username,
        "password": hashed_password
    }

    try:
        with open("users.json", "r") as f:
            users = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        print("Users file not found or corrupt. Creating new list.")
        users = []

    for user in users:
        if user.get("username") == username:
            return False

    # adds new user to list
    users.append(new_user)

    try:
        with open("users.json", "w") as f:
            # recreate users list
            json.dump(users, f, indent=4)
        return True
    except Exception as e:
        print("Error writing to file:", e)
        return False
        


def logout(username):

    print("Thank you for using Safe Vault!")
    input("Press any button to continue...")

    helper.log_action("Logged out", username)