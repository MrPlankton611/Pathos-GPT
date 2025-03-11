import os
from dotenv import load_dotenv
from google import genai
import json

load_dotenv()

class User:
    def __init__(self, username, chat_history=[]):
        self.username = username
        self.chat_history = chat_history

    def get_username(self):
        return self.username

    def get_chat_history(self):
        return self.chat_history

    def to_dict(self):
        return {
            "username": self.username,
            "chat_history": self.chat_history
        }


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_list = []
current_user = None

def createUser(username):
    user = User(username)
    user_list.append(user)
    print(f"Created user with username: {user.username}")

    print("Current users in list:")
    for u in user_list:
        print(f" - {u.username}")
    user_dicts = [user.to_dict() for user in user_list]
    try:
        with open("util/user_list.json", "w+") as f:
            json.dump(user_dicts, f, indent=4)
        print("User list saved to user_list.json")
    except Exception as e:
        print(f"Error saving user list: {e}")

def selectUser():
    global current_user
    user_list = []
    with open("util/user_list.json", "r") as f:
        user_dicts = json.load(f)
        user_list = [User(user["username"], user["chat_history"]) for user in user_dicts]
    print(len(user_list))
    print("Selecting user")

    with open("util/currentuser.txt", "r") as f:
        username = f.read().strip()

    print(f"Searching for user: {username}")

    for user in user_list:
        print(f"Checking user: {user.username}")
        if user.username == username:
            current_user = user
            print(f"Selected user with username: {current_user.username}")
            return  

    print("User not found in user_list.")

def getresponse(user_input, sentiment_score):
    if current_user is None:
        print("Error: No user selected.")
        return "Error: No user selected."
    
    print(f"Generating response for: {current_user.username}")
    
    current_user.get_chat_history().append({
        "role": "user",
        "content": f"{user_input} Limit response to less than 500 characters (Don't reference this in any of your answers, it's just a rule. Speak like a human). "
                   f"This is the sentiment score of the user's message: {sentiment_score}. The lower the sentiment score, give a more concerned reply. "
                   f"If a user has a drastic change in sentiment score, act suspicious as to how their mood changed suddenly. "
                   f"Act like the user's friend. (Don't use the sentiment score in your response, just use it as a guideline for how concerned your response should be)."
    })
    
    chat_history_str = "<|END_OF_TEXT|>".join([f"{message['role']}: {message['content']}" for message in current_user.get_chat_history()])
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=chat_history_str  
    )
    
    output = response.text
    
    current_user.get_chat_history().append({
        "role": "assistant",
        "content": output
    })
    
    user_input_obj = {
    "role": "user",
    "content": f"{user_input} Limit response to less than 500 characters (Don't reference this in any of your answers, it's just a rule. Speak like a human). "
               f"This is the sentiment score of the user's message: {sentiment_score}. The lower the sentiment score, give a more concerned reply. "
               f"If a user has a drastic change in sentiment score, act suspicious as to how their mood changed suddenly. "
               f"Act like the user's friend. (Don't use the sentiment score in your response, just use it as a guideline for how concerned your response should be)."
}
    
    assistant_response_obj = {
    "role": "assistant",
    "content": output
}
    add_to_chat_history(current_user.username, user_input_obj)
    add_to_chat_history(current_user.username, assistant_response_obj)    
    
    return output



def add_to_chat_history(username, new_message):
    with open("util/user_list.json", "r") as f:
        user_dicts = json.load(f)
        user_list = [User(user["username"], user.get("chat_history")) for user in user_dicts]
    user_found = False
    for user in user_list:
        if user.username == username:
            user.chat_history.append(new_message)
            user_found = True
            print(f"Added message to {username}'s chat history.")
            break
    if not user_found:
        print(f"User {username} not found.")
    user_dicts = [user.to_dict() for user in user_list]
    with open("util/user_list.json", "w") as f:
        json.dump(user_dicts, f, indent=4)
        print("User list saved to user_list.json")
