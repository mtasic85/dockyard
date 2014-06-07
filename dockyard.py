# -*- coding: utf-8 -*-

'''
Master listens on port default 8000, but it is indtended to run on port 80.
It is web app that manages slaves.
It allows users to register, and manage their instances/containers.
Admin is allowed to modify many aspects of web app.

Sections:
    Dashboard
        - live stats
        - earning [super-only]
        - spending [user-only]
    
    Hosts [super]
        - list
        - add
        - remove
        - update
    
    Images [per-user, or all for super]
        - list
        - add
        - remove
        - update
    
    Volumes
        - list
        - add
        - remove
    
    Containers [per-user, or all for super]
        - list
        - create
        
        - clone
        - destory
        - start
        - restart
        - stop
        - attach
        - logs
    
    Networking
        - list
        - add
        - remove
        - update
    
    Settings [super]
        - set title
        - set logo
    
    Profile
        - update
'''

__all__ = ['app']
import os
import sys

# requests
import requests

# werkzeug
from werkzeug.contrib.fixers import ProxyFix

# flask
from flask import (
    Flask, request, session, g,
    redirect, url_for, abort,
    render_template, flash, jsonify,
    Blueprint, abort,
    send_from_directory,
    current_app,
)

# flask login
from flask.ext.login import (
    current_user, login_required, fresh_login_required,
    login_user, logout_user, confirm_login,
)

# config
from config import FlaskConfig

# app
app = Flask(__name__)

if FlaskConfig.PROXY_FIX:
    app.wsgi_app = ProxyFix(app.wsgi_app)

app.config.from_object(FlaskConfig)

@app.route('/', methods=['GET'])
def index():
    return ''

if __name__ == '__main__':
    import argparse
    
    # parse cli arguments
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-b', '--bind', type=str,
                        default='{HOST}:{PORT}'.format(**FlaskConfig.__dict__),
                        help='bind to host:port')
    
    parser.add_argument('-t', '--threaded', type=bool,
                        default=FlaskConfig.THREADED,
                        help='threaded execution')
    
    args = parser.parse_args()
    
    # host, port
    host_port = args.bind.split(':')
    
    if len(host_port) == 1:
        host = host_port[0]
        port = FlaskConfig.PORT
    else:
        host = host_port[0]
        port = int(host_port[1])
    
    FlaskConfig.HOST = host
    FlaskConfig.PORT = port
    FlaskConfig.THREADED = args.threaded
    
    # run app
    app.run(
        host = FlaskConfig.HOST,
        port = FlaskConfig.PORT,
        threaded = FlaskConfig.THREADED,
    )
