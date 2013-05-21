import os
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug import secure_filename
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['pcap'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/ssl-monitor/")
def index():
    if not session.get('uid', None):
        session['uid'] = uuid.uuid4().hex

    return render_template("index.html")


@app.route("/ssl-monitor/replay/", methods=['POST', 'GET'])
def replay():
    if not session.get('uid', None):
        session['uid'] = uuid.uuid4().hex

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(str(session['uid']))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('game',
                                    filename=filename))
            
    return render_template("replay.html")


@app.route("/ssl-monitor/game/")
def game():
    if request.method == 'GET':
        if 'filename' in request.args:
            return request.args.get('filename')

    return render_template("game.html")

if __name__ == "__main__":
    app.secret_key = 'bill gates is gay!'
    app.run(debug=True)
