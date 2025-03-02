import os
from dotenv import load_dotenv #type:ignore
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chat_history = []

def getresponse(user_input, sentiment_score):
    global chat_history
    chat_history.append({"role": "user", "content": user_input+f" Limit response less than 500 characters(Dont reference this in any of your answers, its just a rule, speak like a human ). This is the sentiment score of the user's message, {sentiment_score}. The lower the sentiment score, give a more concerned reply. If a user has a drastic change in sentiment score, act suspicious as to how their mood changed suddenly. Act like the user's friend."})

    chat_history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=chat_history_str
    )

    output = response.text
    output = output.replace("*", "\n -")

    chat_history.append({"role": "assistant", "content": output})
    
    return output
