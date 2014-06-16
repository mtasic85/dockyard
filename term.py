# -*- coding: utf-8 -*-
__all__ = ['term_blueprint']
from datetime import datetime, timedelta

# dateutil
from dateutil.parser import parse as dtparse

# flask
from flask import (
    Flask, request, session, g,
    redirect, url_for, abort,
    render_template, flash, jsonify,
    Blueprint, abort,
    send_from_directory,
    current_app,
)

# flask login
from flask.ext.login import login_required, fresh_login_required, current_user

# flask-wtf
from flask.ext.wtf import Form
from wtforms import validators
from wtforms import TextField, PasswordField, SelectField, BooleanField
from wtforms_html5 import EmailField

# model
from model.db import db
from model.db import object_to_dict, objects_to_list, update_object_with_dict
from model.user import UserAccount, UserQuota

term_blueprint = Blueprint('term_blueprint', __name__)

@term_blueprint.route('/term/<host>/<int:port>', methods=['GET'])
# @login_required
def term_term(host, port):
    # username = current_user.username
    print 'term_term:', locals()
    
    host = host.replace('_', '.')
    
    # get user account properties
    # user_account = UserAccount.query.filter_by(username=username).one()
    # dct = object_to_dict(user_account)
    
    return render_template(
        'term-term.html',
        host = host,
        port = port,
        # **dct
    )

"""
@term_blueprint.route('/terms/all', methods=['POST'])
@login_required
def term_terms_all():
    username = current_user.username
    usertype = current_user.usertype
    print 'term_terms_all:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    terms = Host.query.all()
    _terms = objects_to_list(terms)
    
    data = {
        'terms': _terms,
    }
    
    return jsonify(data)

@term_blueprint.route('/term/create', methods=['POST'])
@login_required
def term_create():
    username = current_user.username
    usertype = current_user.usertype
    _term = request.json['term']
    print 'term_add:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    term = Host(**_term)
    _term['created'] = _term['updated'] = datetime.utcnow()
    db.session.add(term)
    db.session.commit()
    
    _term = object_to_dict(term)
    
    data = {
        'term': _term,
    }
    
    return jsonify(data)

@term_blueprint.route('/term/update', methods=['POST'])
@login_required
def term_update():
    username = current_user.username
    usertype = current_user.usertype
    _term = request.json['term']
    print 'term_update:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    term = Host.query.get(_term['id'])
    _term['updated'] = datetime.utcnow()
    update_object_with_dict(term, _term)
    db.session.commit()
    
    _term = object_to_dict(term)
    
    data = {
        'term': _term,
    }
    
    return jsonify(data)

@term_blueprint.route('/term/remove', methods=['POST'])
@login_required
def term_remove():
    username = current_user.username
    usertype = current_user.usertype
    id = request.json['id']
    print 'term_remove:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    term = Host.query.get(id)
    db.session.delete(term)
    db.session.commit()
    
    data = {}
    return jsonify(data)
"""
