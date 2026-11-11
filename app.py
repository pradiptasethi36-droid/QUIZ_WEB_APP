from flask import Flask, render_template, redirect, url_for, request, session
import random
from questions import QUESTIONS

app = Flask(__name__)
app.secret_key = "change-this-secret-key"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session["questions"] = random.sample(QUESTIONS, len(QUESTIONS))
        session["score"] = 0
        session["current"] = 0
        return redirect(url_for("play"))

    return render_template("home.html")


@app.route("/play", methods=["GET", "POST"])
def play():
    questions = session.get("questions")

    if not questions:
        return redirect(url_for("home"))

    index = session.get("current", 0)

    if index >= len(questions):
        return redirect(url_for("result"))

    question = questions[index]

    if request.method == "POST":
        if request.form.get("answer") == question["answer"]:
            session["score"] += 1

        session["current"] = index + 1

        if session["current"] >= len(questions):
            return redirect(url_for("result"))

        return redirect(url_for("play"))

    return render_template(
        "play.html",
        question=question,
        number=index + 1,
        total=len(questions),
    )


@app.route("/result")
def result():
    questions = session.get("questions")

    if not questions:
        return redirect(url_for("home"))

    score = session.get("score", 0)
    total = len(questions)

    return render_template(
        "result.html",
        score=score,
        total=total,
    )


if __name__ == "__main__":
    app.run(debug=True)