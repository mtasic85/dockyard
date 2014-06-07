# -*- coding: utf-8 -*-

'''
Slave is server that listens to default port 4000.
Master asks slave for stats and to execute commands.
'''

__all__ = ['app']
import os
import sys

# requests with 'http+unix:/' adapter
# based on dotcloud/docker-py
import socket
import requests
import requests.adapters

try:
    import http.client as httplib
except ImportError:
    import httplib

try:
    import requests.packages.urllib3.connectionpool as connectionpool
except ImportError:
    import urllib3.connectionpool as connectionpool

class UnixAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, base_url, timeout=60):
        self.base_url = base_url
        self.timeout = timeout
        super(UnixAdapter, self).__init__()
    
    def get_connection(self, socket_path, proxies=None):
        return UnixHTTPConnectionPool(self.base_url, socket_path, self.timeout)

class UnixHTTPConnectionPool(connectionpool.HTTPConnectionPool):
    def __init__(self, base_url, socket_path, timeout=60):
        connectionpool.HTTPConnectionPool.__init__(self, 'localhost',
                                                   timeout=timeout)
        self.base_url = base_url
        self.socket_path = socket_path
        self.timeout = timeout

    def _new_conn(self):
        return UnixHTTPConnection(self.base_url, self.socket_path,
                                  self.timeout)

class UnixHTTPConnection(httplib.HTTPConnection, object):
    def __init__(self, base_url, unix_socket, timeout=60):
        httplib.HTTPConnection.__init__(self, 'localhost', timeout=timeout)
        self.base_url = base_url
        self.unix_socket = unix_socket
        self.timeout = timeout

    def connect(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self.base_url.replace("http+unix:/", ""))
        self.sock = sock

    def _extract_path(self, url):
        # remove the base_url entirely..
        return url.replace(self.base_url, "")

    def request(self, method, url, **kwargs):
        url = self._extract_path(self.unix_socket)
        super(UnixHTTPConnection, self).request(method, url, **kwargs)

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
    make_response,
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

@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    # get docker API route
    s = request.url.find(request.url_root) + len(request.url_root)
    path = request.url[s:]
    
    # execute
    s = requests.Session()
    s.mount('http+unix://', UnixAdapter('http+unix://var/run/docker.sock'))
    f = getattr(s, request.method.lower())
    r = f('http+unix://var/run/docker.sock/%s' % path)
    return make_response(r.text, r.status_code, r.headers.items())

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
