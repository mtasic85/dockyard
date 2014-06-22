# -*- coding: utf-8 -*-
__all__ = ['Host']

from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

from .db import get_db
db = get_db()

class Host(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    active =        db.Column(db.Boolean, default=True)
    created =       db.Column(db.DateTime, default=datetime.utcnow)
    updated =       db.Column(db.DateTime)
    
    name =          db.Column(db.String(128))
    host =          db.Column(db.String(128))
    port =          db.Column(db.Integer)
    auth_username = db.Column(db.String(64), default='')
    auth_password = db.Column(db.String(64), default='')
    ram_capacity =  db.Column(db.String(64), default='0')
    ram_reserved =  db.Column(db.String(64), default='0')
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    
    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)
