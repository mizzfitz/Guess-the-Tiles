import random

from flask import Flask, render_template, request, session
from flask_session import Session

class Tiles:
    def __init__(self, guess):
        self.guess = list(guess)

class Guess(Tiles):
    def __init__(self, guess, hint):
        Tiles.__init__(self, guess)
        self.hint = list(hint)

def random_col():
    collors = {0:"Red", 1:"Blue", 2:"Green", 3:"Yellow", 4:"Black", 5:"White"}
    x = random.randint(0, 5)
    return collors.get(x)

def hide_tiles():
    guess = []
    for i in range(4):
        guess.append(random_col())
    return guess

def guess(collors, secret):
    hint = []
    guessed = list(collors)
    hidden = list(secret.guess)
    for i in range(4):
        if (guessed[i] == hidden[i]):
            hint.append("Black")
            hidden[i] = ""
    for i in range(4):
        if (guessed[i] in hidden):
            hint.append("White")
            k = 0
            while (k < 4):
                if (hidden[k] == guessed[i]):
                    hidden[k] = ""
                    break
                else:
                    k += 1
    while (len(hint) < 4):
        hint.append("Gray")

    return Guess(collors, hint)

def check_win(guessObj):
    if ("Black" in guessObj.hint) and ("White" not in guessObj.hint) and ("Gray" not in guessObj.hint):
        return True
    else:
        return False

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["POST", "GET"])
def index():
    if session.get("guesses") is None:
        session["guesses"] = []
        session["answer"] = Tiles(hide_tiles())
    if (request.method == "POST"):
        collors = [request.form.get("col1"), request.form.get("col2"), request.form.get("col3"), request.form.get("col4")]
        guessObj = guess(collors, session["answer"])
        if check_win(guessObj):
            return render_template("win.html", guess=guessObj)
        else:
            session["guesses"].append(guessObj)
            return render_template("index.html", guesses=session["guesses"])
    else:
        session["answer"] = Tiles(hide_tiles())
        session["guesses"] = []
        return render_template("index.html", guesses=session["guesses"])

