
from flask import Flask, render_template, request, jsonify, session #type:ignore
import genapi, audio
import os
import json
import sentiment

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login-page")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signout")
def signout_process():
    session.pop("username", None)
    with open ("util/currentuser.txt", "w") as f:
        f.write("")
    return render_template("login.html")

@app.route("/signup-process", methods=["POST", "GET"])
def signup_process():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        with open("util/login1.json", "r") as f:
            file_data = json.load(f)
            # data = {
            #     username: {
            #         "password": password,
            #     },
            # }
            # file_data = jsonify(file_data)
        print(file_data)
        file_data["accounts"][username] = password
        genapi.createUser(username)
        with open("util/login1.json", "w", encoding="utf-8") as f:
            json.dump(file_data, f, indent = 4)
        session['username'] = username
        return render_template("login.html")

@app.route("/login-process", methods=["POST", "GET"])
def login_process():
    if request.method == "POST":
        id = request.form.get("username")
        password = request.form.get("password")
        with open("util/login1.json", "r") as f:
            file_data = json.load(f)
            file_data=file_data["accounts"]
            usernames = file_data.keys()
            if id in usernames:
                if password == file_data[id]:
                    session['username'] = id
                    with open("util/currentuser.txt", "w") as f:
                        f.write(id)
                    genapi.selectUser()
                    return render_template("index.html")
                else:
                    return render_template("login.html")
            else:
                return render_template("login.html", message="Incorrect username or password")

@app.route("/send_message", methods=["POST"])
def send_message():
    print("hi")
    user_input = request.json.get("message")
    sentiment_score = sentiment.compute_sentiment(user_input)
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    ai_response = genapi.getresponse(user_input, sentiment_score)
    
    audio.playaudio(ai_response)

    print(ai_response)
    
    return jsonify({"ai_message": ai_response})



if __name__ == "__main__":
    app.run(debug=True)
