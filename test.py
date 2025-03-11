
user_input = "this is user input"
sentiment_score = 5

output = "Output"

current_input = [
        {
        "role": "user",
        "content": f"{user_input} Limit response to less than 500 characters (Don't reference this in any of your answers, it's just a rule. Speak like a human). "
                   f"This is the sentiment score of the user's message: {sentiment_score}. The lower the sentiment score, give a more concerned reply. "
                   f"If a user has a drastic change in sentiment score, act suspicious as to how their mood changed suddenly. "
                   f"Act like the user's friend. (Don't use the sentiment score in your response, just use it as a guideline for how concerned your response should be)."
        },

        {
        "role": "assistant",
        "content": output
        }
    ]

print(current_input[-2:])