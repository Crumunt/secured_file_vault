import json
import os
from datetime import datetime

def log_action(action, username):

    with open("logs/vault_log.txt", "a") as log_file:
        log_file.write(f"{username} - {action} - {datetime.now()} \n")

    

def get_file_collection(username):
    if not os.path.exists("user_files.json"):
        return []
    with open("user_files.json", "r") as f:

        user_files = json.load(f)

    for user in user_files:
        if user.get('username') == username:
            return user
 

def load_user_files(filename="user_files.json"):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_users(user_files, filename="user_files.json"):
    try:
        with open(filename, "w") as f:
            json.dump(user_files, f, indent=4)
    except Exception as e:
        input(f"Error: {e}")
    


def add_user_file_record(file_name, encryption_key, username, filename="user_files.json"):
    user_files = load_user_files(filename)

    encryption_key = encryption_key.decode('utf-8')

    user_entry = next((u for u in user_files if u.get("username") == username), None)

    if not user_entry:
        user_entry = {"username": username, "files": []}
        user_files.append(user_entry)

    
    user_entry["files"].append({
        "file_name": file_name,
        "encryption_key": encryption_key
    })

    save_users(user_files, filename)
    
    return True

def remove_user_file_record(file_name, username):
    users = load_user_files()

    user = next((u for u in users if u["username"] == username), None)
    if not user:
        return False

    # Filter out the file to remove
    original_count = len(user["files"])
    user["files"] = [f for f in user["files"] if f["file_name"] != file_name]


    if len(user["files"]) == original_count:
        print(f"File '{file_name}' not found for user '{username}'.")
        return False
    

    save_users(users)