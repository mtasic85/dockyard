# -*- coding: utf-8 -*-
__all__ = ['FlaskConfig']

class FlaskConfig(object):
    SECRET_KEY = '!d0cky4rd-sl4ve!'   # IMPORTANT: change this value with your secret
    DEBUG = True
    SILENT = False
    PROXY_FIX = True
    HOST = '0.0.0.0'
    PORT = 4000
    THREADED = False
    LAZY_INITIALIZATION = False
    # DEFAULT_VIEW = 'home_blueprint.home'
    
    # login
    # LOGIN_VIEW = 'account_blueprint.account_signin'
    
    # database
    # SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@127.0.0.1/db'

