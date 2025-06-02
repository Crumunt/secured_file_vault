from cryptography.fernet import Fernet
import os
import helper

def encrypt(filepath, username):


    file_name = os.path.basename(filepath)

    filepath = filepath.replace("\\", "/")

    helper.log_action(f"Encrypting file - '{file_name}'", username)
    try:
        # subukan na'tin buksan ge
        with open(filepath, "rb") as f:
            original = f.read()

        key = Fernet.generate_key()

        # record yung data
        # depende sa username, naka save lahat ng files n'ya doon ge
        helper.add_user_file_record(file_name, key, username, "user_files.json")

        fernet = Fernet(key)

        # encrypt malamang
        encrypted_file = fernet.encrypt(original)

        # try ulit mag write naman ge
        with open(f"encrypted_files/{file_name}", "wb") as f:
            f.write(encrypted_file)


        helper.log_action(f"File '{file_name}' encrypted", username)

        return True
    except:
        helper.log_action(f"Failed to encrypt '{file_name}'", username)
        input("Something went wrong...")
        return False


    
    
   

def decrypt(file_index, username):

    file_collection = helper.get_file_collection(username)

    file_name = file_collection["files"][file_index]["file_name"]
    key = file_collection["files"][file_index]["encryption_key"]

    filepath = f"encrypted_files/{file_name}"

    fernet = Fernet(key)

    helper.log_action(f"Decrypting '{file_name}'", username)

    try:

        with open(filepath, "rb") as f:
            encrypted_file = f.read()

        decrypted_file = fernet.decrypt(encrypted_file)   

        with open(f"decrypted_files/{file_name}", "wb") as f:
            f.write(decrypted_file)


        if os.path.exists(filepath):
            os.remove(filepath)

        # REMOVES FILE FROM JSON PAKSHIET
        helper.remove_user_file_record(file_name, username)   

    except Exception as e:
        helper.log_action(f"ERROR Decrypting '{file_name}'", username)
        input(f"Something went wrong {e}")
        return False
    

    helper.log_action(f"File '{file_name}' decrypted", username)

    return True


