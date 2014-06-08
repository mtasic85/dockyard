# -*- coding: utf-8 -*-
__all__ = ['HTTPRoute', 'HTTPRouteHost']

from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

from .db import get_db
db = get_db()

class HTTPRoute(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    active =        db.Column(db.Boolean, default=True)
    created =       db.Column(db.DateTime, default=datetime.utcnow)
    updated =       db.Column(db.DateTime)
    
    username =      db.Column(db.String(128))
    domain =        db.Column(db.String(1024), unique=True)
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    
    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)

class HTTPRouteHost(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    active =        db.Column(db.Boolean, default=True)
    created =       db.Column(db.DateTime, default=datetime.utcnow)
    updated =       db.Column(db.DateTime)
    
    http_route_id = db.Column(db.Integer, unique=True)
    host_id =       db.Column(db.Integer, unique=True)
    port =          db.Column(db.Integer)
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    
    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)
