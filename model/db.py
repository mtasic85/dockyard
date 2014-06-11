# -*- coding: utf-8 -*-
__all__ = ['db', 'init_app', 'get_db', 'object_to_dict', 'objects_to_list',
           'update_object_with_dict']

from datetime import date, time, datetime

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

def object_to_dict(obj, skip=()):
    dct = {}
    
    for column in obj.__table__.columns:
        name = column.name
        
        if name in skip:
            continue
        
        v = getattr(obj, name)
        
        if isinstance(v, date) or isinstance(v, time) or \
           isinstance(v, datetime):
            v = v.isoformat()
        
        dct[name] = v
    
    return dct

def objects_to_list(objs, skip=()):
    return [object_to_dict(obj, skip) for obj in objs]

def update_object_with_dict(obj, dct, skip=()):
    for k, v in dct.items():
        if k in skip:
            continue
        
        # FIXME: support date, time, and datetime objects
        
        setattr(obj, k, v)
