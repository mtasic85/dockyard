# -*- coding: utf-8 -*-
__all__ = ['Volume']

from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

from .db import get_db
db = get_db()

class Volume(db.Model):
    id =                db.Column(db.Integer, primary_key=True)
    active =            db.Column(db.Boolean, default=True)
    created =           db.Column(db.DateTime, default=datetime.utcnow)
    updated =           db.Column(db.DateTime)
    
    host_id =           db.Column(db.Integer)
    mount_point_id =    db.Column(db.Integer)
    username =          db.Column(db.String(128))
    name =              db.Column(db.String(256))
    perm_name =         db.Column(db.String(256))
    capacity =          db.Column(db.String(32), default='1G')
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    
    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)
