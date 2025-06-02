import os
import shutil
import time
from cryptography.fernet import Fernet
import helper

def zip_folder(folder_path,username):

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    zip_name = f"{username}_batch_{timestamp}"

    shutil.make_archive(f"zipped_folders/{zip_name}", 'zip', folder_path)

    return zip_name

def encrypt_folder(folder_path, username):

    folder_path = folder_path.replace("\\", "/")

    zip_name = zip_folder(folder_path, username)
     
    with open(f"zipped_folders/{zip_name}.zip", "rb") as f:
        data = f.read()

    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    helper.log_action(f"Batch Encrypting '{zip_name}'", username)

    helper.add_user_file_record(f"{zip_name}.zip.encrypted", key, username, "user_files.json")

    with open(f"encrypted_files/{zip_name}.zip.encrypted", "wb") as f:
        f.write(encrypted)

    os.remove(f"zipped_folders/{zip_name}.zip")

    helper.log_action(f"Folder '{zip_name}' encrypted", username)

    return True


def decrypt_folder(file_index, username):
    file_collection = helper.get_file_collection(username)

    file_name = file_collection["files"][file_index]["file_name"]
    key = file_collection["files"][file_index]["encryption_key"]

    filepath = f"encrypted_files/{file_name}"

    fernet = Fernet(key)

    helper.log_action(f"Decrypting folder '{file_name}'", username)

    with open(f"{filepath}", "rb") as f:
        encrypted_data = f.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    # Write the decrypted data back to a .zip file
    with open(f"zipped_folders/{file_name}.zip", "wb") as f:
        f.write(decrypted_data)

    # Extract the zip file
    shutil.unpack_archive(f"zipped_folders/{file_name}.zip", "decrypted_files/", 'zip')

    # clean up the intermediate .zip file
    os.remove(f"encrypted_files/{file_name}")
    os.remove(f"zipped_folders/{file_name}.zip")

    # remove json file record
    helper.remove_user_file_record(file_name, username) 

    helper.log_action(f"Folder '{file_name}' decrypted", username)

    # medjo fucked yung extensions di na umabot sa time para maayos
    # nagiging .zip.encrypted tas kapag binalik sa zip, hindi nawawala yung .zip.encryted na extension
    # nadadagdagan lang ng .zip sa dulo HAHAHAHHAHAHA

    return True
