from flask import render_template, request, session, flash, url_for, redirect
from functools import wraps

from pymongo import MongoClient

import hashlib
import json
import config


dbc = MongoClient("127.0.0.1")



def logged_in():
    if not 'logged_in' in session or not session['logged_in'] is True:
        return False
    return True

def salted_hash(s):
    passwordhash = hashlib.sha1()
    passwordhash.update(unicode(s) + config.SHA1_SALT)
    passwordhash = unicode(passwordhash.hexdigest())
    return passwordhash

def login(email, password):
    user = dbc.ssl_monitor.users.find_one({'email': email})
    
    if not user:
        
        return False

    passwordhash = salted_hash(password)

    if (user is None or user['password'] != passwordhash):
        return False
    else:
        session['logged_in'] = True
        session['user'] = user
    return True


def logout():
    del session['logged_in']
    del session['user']

def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not logged_in():
            return redirect(url_for("login_user"))
        return func(*args, **kwargs)
    return decorated_view
