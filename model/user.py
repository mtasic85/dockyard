# -*- coding: utf-8 -*-
__all__ = ['UserAccount', 'UserQuota', 'UserStat']

from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

from .db import get_db
db = get_db()

class UserAccount(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    active =        db.Column(db.Boolean, default=True)
    created =       db.Column(db.DateTime, default=datetime.utcnow)
    updated =       db.Column(db.DateTime)
    
    usertype =      db.Column(db.String(64))
    username =      db.Column(db.String(64), unique=True)
    email =         db.Column(db.String(128), unique=True)
    password =      db.Column(db.String(64))
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    
    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.username)

class UserQuota(db.Model):
    id =                    db.Column(db.Integer, primary_key=True)
    active =                db.Column(db.Boolean, default=True)
    created =               db.Column(db.DateTime, default=datetime.utcnow)
    updated =               db.Column(db.DateTime)
    username =              db.Column(db.String(64), unique=True)
    
    # image
    n_images =              db.Column(db.Integer, default=10)
    
    # volume
    n_volumes =             db.Column(db.Integer, default=10)
    max_volume_cap =        db.Column(db.Integer, default=1)
    max_volumes_cap =       db.Column(db.Integer, default=10)
    
    # container
    n_containers =          db.Column(db.Integer, default=10)
    max_container_cpu =     db.Column(db.Integer, default=10)
    max_containers_cpu =    db.Column(db.Integer, default=10)
    max_container_ram =     db.Column(db.Integer, default=128)
    max_containers_ram =    db.Column(db.Integer, default=1280)
    
    # subdomain
    n_subdomains =          db.Column(db.Integer, default=2)
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    
    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)

class UserStat(db.Model):
    id =                    db.Column(db.Integer, primary_key=True)
    active =                db.Column(db.Boolean, default=True)
    created =               db.Column(db.DateTime, default=datetime.utcnow)
    updated =               db.Column(db.DateTime)
    username =              db.Column(db.String(64), unique=True)
    
    # image
    n_images =              db.Column(db.Integer, default=0)
    
    # volume
    n_volumes =             db.Column(db.Integer, default=0)
    volumes_cap =           db.Column(db.Integer, default=0)
    
    # container
    n_containers =          db.Column(db.Integer, default=0)
    containers_cpu =        db.Column(db.Integer, default=0)
    containers_ram =        db.Column(db.Integer, default=0)
    
    # subdomain
    n_subdomains =          db.Column(db.Integer, default=0)
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    
    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)
