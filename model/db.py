# -*- coding: utf-8 -*-
__all__ = ['db', 'init_app', 'get_db']

from flask import Flask, current_app
from flask.ext.sqlalchemy import SQLAlchemy

db = None

def init_db(app):
    global db
    
    if db is None:
        db = SQLAlchemy(app)
    
    return db

def get_db():
    global db
    return db
