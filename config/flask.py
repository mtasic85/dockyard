# -*- coding: utf-8 -*-
__all__ = ['FlaskConfig']

class FlaskConfig(object):
    SECRET_KEY = '!d0cky4rd!'   # IMPORTANT: change this value with your secret
    DEBUG = True
    SILENT = False
    PROXY_FIX = True
    HOST = '0.0.0.0'
    PORT = 8000
    THREADED = False
    LAZY_INITIALIZATION = False
    DEFAULT_VIEW = 'dashboard_blueprint.dashboard_dashboard'
    
    # login
    LOGIN_VIEW = 'account_blueprint.account_signin'
    
    # database
    SQLALCHEMY_DATABASE_URI = 'mysql://dockyard:d0cky4rd@127.0.0.1/dockyard'
