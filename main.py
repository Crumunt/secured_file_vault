import os
import pwinput
import auth
import batch_processor
import helper
import vault

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    clear_screen()

    print("🔐 Welcome to Secure File Vault")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    
    try:
        option = int(input("Choose an option: "))
    except ValueError:
        print("Please only enter numbers!")
        main()

    if option not in range(1,4):
        print("Option not valid!")
        main()

    toggle_screen(option)

    
def toggle_screen(option):
    if option == 1:
        toggle_login()
    elif option == 2:
        toggle_register()
    else:
        print("Thank you for using Secure File Vault")


def toggle_login():
    clear_screen()

    username = input("Enter Username: ")
    password = pwinput.pwinput(prompt='Enter password: ', mask='*')

    if not auth.login(username, password):
        print("Username/Password is incorrect!")
        input("press any button to continue...")
        main()
    
    print("User credentials have been verified!")
    input("Press any button to continue...")
    toggle_main_screen(username)

def toggle_register():
    clear_screen()

    username = input("Enter Username: ")
    password = input("Enter Password: ")
    confirm_password = input("Confirm Password: ")

    if not auth.register(username, password, confirm_password):
        print("Something went wrong!")
        print("Please try again.")
        input("Please press any button to continue.")
    else:
        print("User succefully registered!")
        input("Press any button to continue.")
    
    main()



def toggle_main_screen(username):
    
    while True:
        clear_screen()
    
        print("📦 Vault Menu")
        print("1. 🔒 Encrypt File")
        print("2. 📂 Batch Encryption")
        print("3. 🔓 Decrypt File")
        print("4. 📂 View Encrypted Files")
        print("5. 📜 View Logs")
        print("6. 🚪 Logout")
        
        try:
            choice = int(input("Choose an option: "))
            
            if choice not in range(1,7):
                print("Invalid Option! Please choose a number from 1 to 6")
                raise ValueError

        except ValueError:
            print("Invalid input!")
            print("Please choose from the numbered options above.")
            input("Press any button to continue...")
            continue


        if not toggle_menu(choice, username):
            break
        


def toggle_menu(choice, username):
    
    clear_screen()


    if choice == 1:
        while True:
            filepath = input("Enter filepath: ")
            if vault.encrypt(filepath, username):
                print("File encrypted successfully!")
                input("Press any button to continue...")
                return True
            else:
                print("An error has occurred!")
                print("Please try again.")
                input("Press any button to continue...")
        

    elif choice == 2:
        clear_screen()

        while True:
            filepath = input("Enter filepath: ")
            if batch_processor.encrypt_folder(filepath, username):
                print("File encrypted successfully!")
                input("Press any button to continue...")

                return True
            else:
                print("An error has occurred!")
                print("Please try again.")
                input("Press any button to continue...")

    elif choice == 3:
        
        while True:

            clear_screen()

            file_collection = helper.get_file_collection(username)

            print(f"{username}'s vault")
            for index, user_files in enumerate(file_collection["files"]):
                print(f"[{(index+1)}]: {user_files['file_name']}")



            print("[0]: Return to main screen")

            try:
                choice = int(input("Enter file number: "))

                if(choice == 0):
                    # toggle_main_screen(username)
                    return True

                if choice not in range(1, (len(file_collection["files"])  + 1)):
                    raise ValueError

            except ValueError:
                print("An error has occurred!")
                print("Please try again.")
                input("Press any button to continue...")

            
            file_index = choice - 1

            file_name = file_collection["files"][file_index]['file_name']

            result = vault.decrypt(file_index, username) if "batch" not in file_name else batch_processor.decrypt_folder(file_index,username)
            
            if result:
                print("File decrypted successfully!")
                input("Press any button to continue...")
                return True
            else:
                print("An error has occurred!")
                print("Please try again.")
                input("Press any button to continue...")

    


    elif choice == 4:

        file_collection = helper.get_file_collection(username)

        print(f"{username}'s vault")
        for index, user_files in enumerate(file_collection["files"]):
            print(f"[{(index+1)}]: {user_files['file_name']}")

        input("Press any button to return...")

        # toggle_main_screen(username)
        return True

    elif choice == 5:
        clear_screen()

        with open("logs/vault_log.txt", "rb") as f:
            logs = f.read()

        print(logs.decode())
        input("Press any button to return...")

        # toggle_main_screen(username)
        return True

    elif choice == 6:
        clear_screen()
        auth.logout(username)

        main()
    else:
        pass

def log_actions():
    pass

main()