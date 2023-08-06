#!/usr/bin/python
# -*- coding: utf-8 -*-
# editor: mufei(ypdh@qq.com tel:+086 15712150708)
'''
Mufei _ __ ___   ___   ___  / _| ___(_)
| '_ ` _ \ / _ \ / _ \| |_ / _ \ |
| | | | | | (_) | (_) |  _|  __/ |
|_| |_| |_|\___/ \___/|_|  \___|_|
'''
__all__ = ['app']

#: python -m pip install python-dotenv
#：python -m moofei.find 127.0.0.1:5000 --webbrowser
#：python find 127.0.0.1:5000 --webbrowser
    

import os, sys, time, re, json
from moofei.valid.flask_valid import *
try:
    from _app import static_file, finds, stopPros, infoPros
    from valid.flask_httpauth import HTTPDigestAuth 
except:
    from moofei._app import static_file, finds, stopPros, infoPros
    from moofei.valid.flask_httpauth import HTTPDigestAuth
from flask import Flask, request
import uuid
app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid1())

users = {"admin": "123456"}    
print(' * Login username And password For:', users)
auth = HTTPDigestAuth(realm='moofei')
    
@auth.get_password
def get_pw(username): 
    return users.get(username)
    
@auth.get_has_ignore
def has_ignore():
    return request.remote_addr=='127.0.0.1' 
           
@app.route("/")
@app.route("/<path>")
@auth.login_required
def index(path=""): 
    return static_file(path)
       
@app.route("/get_find", methods=["POST"])
@auth.login_required
def get_find(): 
    return call_request_wrap(infoPros)()    
    
@app.route("/stop_find", methods=["POST"])
@auth.login_required
def stop_find(): 
    return call_request_wrap(stopPros)() 
               
@app.route("/find", methods=["POST"])
@auth.login_required
def find_files_or_words():
    backupdir = './.backup'
    return call_request_wrap(finds)(backupdir=backupdir)
       
@app.route("/find_download")
@auth.login_required
def find_download(): 
    fpath = request.args.get('file')
    as_attachment = False if  request.args.get('is_view') else True
    return static_file(fpath, is_static=0, as_attachment=as_attachment) 




if __name__ == "__main__":
    try:
        import colorama; colorama.init(autoreset=True, wrap=True)
    except ImportError:
        pass    
    app.run(debug=True) #host='0.0.0.0',

    