import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
import subprocess
from config import FIREBASE_CREDENTIALS_PATH, GEMINI_API_KEY

# Firebase initialization
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def check_and_execute_command(command_name):
    """
    Checks if a command exists. If not, prompts user to create it,
    generates code suggestions with Gemini, and stores the command.
    """
    command_ref = db.collection("custom_commands").document(command_name)
    command_doc = command_ref.get()

    # Step 1: Check if the command exists
    if command_doc.exists:
        # Execute existing command
        command_action = command_doc.to_dict()["action"]
        subprocess.run(command_action, shell=True)
        print(f"Executed existing command '{command_name}'.")
    else:
        # Step 2: Prompt user to define new command
        user_confirm = input(f"The command '{command_name}' does not exist. Would you like to create it? (yes/no): ")
        if user_confirm.lower() == "yes":
            # Step 3: Get command description from the user
            command_description = input(f"Please describe what '{command_name}' should do: ")

            try:
                # Step 4: Pass command description to Gemini
                gemini_response = model.generate_content("Suggest a command that can be executed in shell and perform this action : " + command_description + "\nOnly write the command and nothing else. not even quotation marks or endline characters.")
                suggested_command = gemini_response.text.strip()
            except Exception as e:
                print(f"Error generating command suggestion: {e}")
                return None

            # Confirm the suggested command with the user
            print(f"Suggested command: {suggested_command}")
            final_confirm = input("Would you like to save this command? (yes/no): ")
            if final_confirm.lower() == "yes":
                # Step 5: Store the new command in Firestore
                command_ref.set({
                    "action": suggested_command
                })
                print(f"Custom command '{command_name}' added successfully and ready for use.")
        else:
            print("Command creation canceled.")

# Example Usage
if __name__ == "__main__":
    # User initiates command
    user_command = input("Please say your command: ")
    check_and_execute_command(user_command)
