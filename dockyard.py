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
        
        # - clone
        - start
        - restart
        - stop
        - attach
        - logs
        - destory
    
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
from config.flask import FlaskConfig

# app
app = Flask(__name__)

if FlaskConfig.PROXY_FIX:
    app.wsgi_app = ProxyFix(app.wsgi_app)

app.config.from_object(FlaskConfig)

# flask-sqlalchemy
from model.db import init_db
db = init_db(app)

# model
from model.user import UserAccount, UserQuota

# model - create all tables
# db.drop_all()
db.create_all()

# create super user if does not exits
if not UserAccount.query.filter_by(username='admin').count():
    user_account = UserAccount(
        username = 'admin',
        password = 'd0cky4rd',
        email = '',
        usertype = 'super',
    )
    db.session.add(user_account)
    db.session.commit()

# account
from account import account_blueprint, login_manager
app.register_blueprint(account_blueprint)
login_manager.init_app(app)

# dashboard
from dashboard import dashboard_blueprint
app.register_blueprint(dashboard_blueprint)

# host
from host import host_blueprint
app.register_blueprint(host_blueprint)

# image
from image import image_blueprint
app.register_blueprint(image_blueprint)

# volume
from volume import volume_blueprint
app.register_blueprint(volume_blueprint)

# container
from container import container_blueprint
app.register_blueprint(container_blueprint)

# network
from network import network_blueprint
app.register_blueprint(network_blueprint)

@app.route('/')
def index():
    return redirect(url_for(FlaskConfig.DEFAULT_VIEW))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'dockyard', 'img'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon',
    )

@app.route('/robots.txt')
def robots():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'dockyard', 'other'),
        'robots.txt',
        mimetype='text/plain',
    )

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(410)
def gone(e):
    return render_template('410.html'), 410

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

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
