from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "index page"

@app.route("/game")
def game():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
