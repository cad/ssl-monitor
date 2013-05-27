import os
import uuid

from multiprocessing import Process

from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug import secure_filename
from pymongo import MongoClient

from session import MongoSessionInterface
import forms
from auth import *
import auth

app = Flask(__name__)
app.session_interface = MongoSessionInterface(db='ssl_monitor')

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['pcap'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 800 * 1024 * 1024

dbc = MongoClient("127.0.0.1") # MongoDB Client


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


@app.route("/ssl-monitor/dashboard/")
def dashboard():
    return "Dashboard Here! <br> User: %s" % session['user']


@app.route("/ssl-monitor/replay/", methods=['POST', 'GET'])
def replay():
    if not session.get('uid', None):
        session['uid'] = uuid.uuid4().hex

    if request.method == 'POST':
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


@app.route("/ssl-monitor/login/", methods=['POST', 'GET'])
def login_user():
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.form)
        if form.validate():
            print 
            result = auth.login(form.email.data, form.password.data)
            if result:
                flash("You have successfully logged in!", 'success')
                return redirect(url_for("dashboard"))
            else:
                flash("Your email or password is wrong!", 'error')
                

    return render_template("login.html", form=form)


@app.route("/ssl-monitor/register/", methods=['POST', 'GET'])
def register():
    form = forms.UserRegistrationForm()
    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.form)
        if form.validate():
            team = { 
                'email': form.email.data,
                'name': form.name.data,
                'team': form.team.data,
                'country': form.country.data,
                'password': salted_hash(form.password.data),
            }
            if not dbc.ssl_monitor.users.find_one({'email':team['email']}):
                dbc.ssl_monitor.users.insert(team)
                flash("Successfully registered!")
                return redirect(url_for("dashboard"))
            flash("Sorry that email address is already exists!", 'error')
    
    return render_template("register.html", form=form)
        
    

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
