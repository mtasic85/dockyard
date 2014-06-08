# -*- coding: utf-8 -*-
__all__ = ['db', 'init_app', 'get_db', 'object_to_dict', 'objects_to_list']

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

def object_to_dict(obj):
    dct = {}
    
    for column in obj.__table__.columns:
        v = getattr(obj, column.name)
        dct[column.name] = v
    
    return dct

def objects_to_list(objs):
    return [object_to_dict(obj) for obj in objs]
