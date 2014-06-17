# -*- coding: utf-8 -*-

'''
Slave is server that listens to default port 4000.
Master asks slave for stats and to execute commands.
'''

__all__ = ['app']
import os
import sys
import threading
from functools import wraps
from ConfigParser import ConfigParser

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
    make_response, Response
)

'''
# flask login
from flask.ext.login import (
    current_user, login_required, fresh_login_required,
    login_user, logout_user, confirm_login,
)
'''

# tornado
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.wsgi

# pexpect
import pexpect

# config
class FlaskConfig(object):
    SECRET_KEY = '!d0cky4rd-sl4ve!'   # IMPORTANT: change this value with your secret
    DEBUG = True
    SILENT = False
    PROXY_FIX = True
    HOST = '0.0.0.0'
    PORT = 4000
    THREADED = False
    LAZY_INITIALIZATION = False

# app
app = Flask(__name__)

if FlaskConfig.PROXY_FIX:
    app.wsgi_app = ProxyFix(app.wsgi_app)

app.config.from_object(FlaskConfig)

def check_auth(username, password):
    config = ConfigParser()
    config.read(['slave.conf'])
    username_ = config.get('auth', 'username')
    password_ = config.get('auth', 'password')
    return username == username_ and password == password_

def authenticate():
    # Sends a 401 response that enables basic auth
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'},
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        
        return f(*args, **kwargs)
    
    return decorated

@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
@requires_auth
def docker_api(path):
    # get docker API route
    s = request.url.find(request.url_root) + len(request.url_root)
    path = request.url[s:]
    print 'docker_api >>>', path
    
    # execute
    s = requests.Session()
    s.mount('http+unix://', UnixAdapter('http+unix://var/run/docker.sock'))
    f = getattr(s, request.method.lower())
    
    if path.startswith('images/create'):
        t = threading.Thread(
            target = f,
            args = ('http+unix://var/run/docker.sock/%s' % path,),
        )
        t.start()
        return make_response('{}', 200, [('content-type', 'application/json')])
    
    r = f('http+unix://var/run/docker.sock/%s' % path)
    
    print 'docker_api <<<', r.text, r.status_code, r.headers.items()
    return make_response(r.text, r.status_code, r.headers.items())

class TermWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        # print 'check_origin:', self, origin
        return True
    
    def open(self):
        # print 'open:', self
        io_loop = tornado.ioloop.IOLoop.instance()
        
        self.proc = pexpect.spawn(
            os.getenv('SHELL'),
            cwd=os.getenv('HOME'),
        )
        
        io_loop.add_handler(self.proc.child_fd, self._read_master, io_loop.READ)
    
    def _read_master(self, *args):
        # print '_read_master:', self, args
        b = os.read(self.proc.child_fd, 1024)
        message = b.encode('utf-8')
        
        try:
            self.write_message(message)
        except Exception as e:
            print e
            self.close()
    
    def on_message(self, message):
        # print 'on_message:', self, repr(message)
        message = message.replace('\r', '\n')
        message = message.decode('utf-8')
        self.proc.write(message)
    
    def on_close(self):
        # print 'on_close:', self
        io_loop = tornado.ioloop.IOLoop.instance()
        io_loop.remove_handler(self.proc.child_fd)
        self.proc.close(force=True)

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
    
    '''
    # run app
    app.run(
        host = FlaskConfig.HOST,
        port = FlaskConfig.PORT,
        threaded = FlaskConfig.THREADED,
    )
    '''
    
    tr = tornado.wsgi.WSGIContainer(app)
    
    application = tornado.web.Application([
        (r'/dockyard/term', TermWebSocket),
        (r'.*', tornado.web.FallbackHandler, dict(fallback=tr)),
    ])
    
    application.listen(FlaskConfig.PORT)
    tornado.ioloop.IOLoop.instance().start()
