import os
from multiprocessing import Process
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug import secure_filename
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['pcap'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 800 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def spawn_capturer(field_name, pcap):
    import sys
    def parse_uri(uri):
        'amp://192.168.1.1:2000'
        decomposed = uri.replace('/', '').split(":")
        return {'protocol':decomposed[0], 'host':decomposed[1], 'port':int(decomposed[2])}
    path = os.path.join(os.path.dirname(os.path.join(os.path.realpath(__file__))), '..')
    sys.path.append(path)
    import ssl_capturer
        
    uri = parse_uri("amp://212.175.35.222:443")
    service = ssl_capturer.CapturingService(field_name, None, None, uri['host'], uri['port'], mode='pcap', pcap=pcap)
    service.ready()
    print "Replaying Started"
    service.run()
    

@app.route("/ssl-monitor/")
def index():
    if not session.get('uid', None):
        session['uid'] = uuid.uuid4().hex

    return render_template("index.html")


@app.route("/ssl-monitor/replay/", methods=['PUT', 'GET'])
def replay():
    if not session.get('uid', None):
        session['uid'] = uuid.uuid4().hex

    if request.method == 'PUT':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(str(session['uid']))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # saved
                
            p = Process(target=spawn_capturer, args=(filename, file_path))
            p.start()
            print "Proccess has been spawned!"

            return redirect(url_for('game',
                                    field_name=filename))
            
    return render_template("replay.html")


@app.route("/ssl-monitor/game/<field_name>")
def game(field_name=None):
    if request.method == 'GET':
        fieldname = field_name
        if field_name:
            return render_template("game.html", fieldname=fieldname)

    return "Bad request", 400


if __name__ == "__main__":
    app.secret_key = 'bill gates is gay!'
    app.run(debug=True)
