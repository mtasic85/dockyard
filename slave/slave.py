# -*- coding: utf-8 -*-

'''
Slave is server that listens to default port 4000.
Master asks slave for stats and to execute commands.
'''

__all__ = ['app']
import os
import sys

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

# docker
import docker

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    import argparse
    
    # parse cli arguments
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-b', '--bind', type=str, default='0.0.0.0:80',
                        help='bind to host:port')
    
    parser.add_argument('-t', '--threaded', type=bool, default=False,
                        help='threaded execution')
    
    args = parser.parse_args()
    
    # host, port
    host_port = args.bind.split(':')
    
    if len(host_port) == 1:
        host = host_port[0]
        port = 80
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
