from flask import Flask, render_template, request
import random

app = Flask(__name__)

class Tiles:
    def __init__(self, guess):
        self.guess = guess

class Guess(Tiles):
    def __init__(self, guess, hint):
        Tiles.__init__(self, guess)
        self.hint = hint

def random_col():
    collors = {0:"red", 1:"blue", 2:"green", 3:"yellow", 4:"black", 5:"white"}
    x = random.randint(0, 5)
    return collors.get(x)

def hide_tiles():
    guess = []
    for i in range(4):
        guess.append(random_col())
    return guess

def guess(collors, secret):
    hint = ["","","",""]
    for i in range(4):
        if (collors[i] == secret.guess[i]):
            hint[i] = "black"
        elif (collors[i] in secret.guess):
            hint[i] = "white"
        else:
            hint[i] = "gray"

    return Guess(collors, hint)

def check_win(guessObj):
    if ("black" in guessObj.hint) and ("white" not in guessObj.hint) and ("gray" not in guessObj.hint):
        return True
    else:
        return False

answer = Tiles(hide_tiles())
guesses = []

@app.route("/", methods=["POST", "GET"])
def index():
    if (request.method == "POST"):
        collors = [request.form.get("col1"), request.form.get("col2"), request.form.get("col3"), request.form.get("col4")]
        guessObj = guess(collors, answer)
        if check_win(guessObj):
            return render_template("win.html", guess=guessObj)
        else:
            guesses.append(guessObj)
            return render_template("index.html", guesses=guesses)
    else:
        return render_template("index.html", guesses=guesses)

@app.route("/reset", methods=["POST"])
def reset():
    answer = Tiles(hide_tiles())
    guesses = []
    return render_template("index.html", guesses=guesses)
