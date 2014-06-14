# -*- coding: utf-8 -*-
__all__ = ['Container']

from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

from .db import get_db
db = get_db()

class Container(db.Model):
    id =                db.Column(db.Integer, primary_key=True)
    active =            db.Column(db.Boolean, default=True)
    created =           db.Column(db.DateTime, default=datetime.utcnow)
    updated =           db.Column(db.DateTime)
    
    host_id =           db.Column(db.Integer)
    username =          db.Column(db.String(128))
    name =              db.Column(db.String(256))
    image_id =          db.Column(db.Integer)
    command =           db.Column(db.String(4096), default='')
    
    volumes =           db.Column(db.String(1024), default='')
    volumes_from =      db.Column(db.String(1024), default='')
    
    env_vars =          db.Column(db.String(4096), default='')
    expose_ports =      db.Column(db.String(1024), default='')
    publish_ports =     db.Column(db.String(1024), default='')
    link_containers =   db.Column(db.String(1024), default='')
    
    ram_limit =         db.Column(db.String(32), default='256m')
    n_cpu_cores =       db.Column(db.Integer, default=1)
    cpu_share =         db.Column(db.Integer, default=0)
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    
    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)
