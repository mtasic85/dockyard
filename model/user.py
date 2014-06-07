# -*- coding: utf-8 -*-
__all__ = ['UserAccount']

from flask.ext.sqlalchemy import SQLAlchemy

from .db import get_db
db = get_db()

class UserAccount(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    active =        db.Column(db.Boolean, default=True)
    usertype =      db.Column(db.String(64))
    username =      db.Column(db.String(64), unique=True)
    email =         db.Column(db.String(128), unique=True)
    password =      db.Column(db.String(64))
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    
    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.username)
