from flask import Flask, render_template

app = Flask(__name__)

@app.route("/ssl-monitor/")
def index():
    return "Welcome to SSL-Monitor. <br> Innovation and Information Technologies Center - Near East University"

@app.route("/ssl-monitor/game/")
def game():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
