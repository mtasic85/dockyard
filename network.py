# -*- coding: utf-8 -*-
__all__ = ['network_blueprint']
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
from model.network import Domain

network_blueprint = Blueprint('network_blueprint', __name__)

@network_blueprint.route('/network/domains', methods=['GET'])
@login_required
def network_domains():
    username = current_user.username
    print 'network_domains:', locals()
    
    # get user account properties
    user_account = UserAccount.query.filter_by(username=username).one()
    dct = object_to_dict(user_account)
    
    return render_template(
        'network-domain.html',
        **dct
    )

@network_blueprint.route('/network/domains/all', methods=['POST'])
@login_required
def network_domains_all():
    username = current_user.username
    usertype = current_user.usertype
    print 'network_domains_all:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    domains = Domain.query.all()
    _domains = objects_to_list(domains)
    
    data = {
        'domains': _domains,
    }
    
    return jsonify(data)

@network_blueprint.route('/network/domain/create', methods=['POST'])
@login_required
def network_domain_create():
    username = current_user.username
    usertype = current_user.usertype
    _domain = request.json['domain']
    print 'network_domain_create:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    domain = Domain(**_network)
    _domain['created'] = _domain['updated'] = datetime.utcnow()
    db.session.add(domain)
    db.session.commit()
    
    _domain = object_to_dict(domain)
    
    data = {
        'domain': _domain,
    }
    
    return jsonify(data)

@network_blueprint.route('/network/domain/update', methods=['POST'])
@login_required
def network_domain_update():
    username = current_user.username
    usertype = current_user.usertype
    _domain = request.json['domain']
    print 'network_domain_update:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    domain = Domain.query.get(_domain['id'])
    _domain['updated'] = datetime.utcnow()
    update_object_with_dict(domain, _domain)
    db.session.commit()
    
    _domain = object_to_dict(domain)
    
    data = {
        'domain': _domain,
    }
    
    return jsonify(data)

@network_blueprint.route('/network/domain/remove', methods=['POST'])
@login_required
def network_domain_remove():
    username = current_user.username
    usertype = current_user.usertype
    id = request.json['id']
    print 'network_domain_remove:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    domain = Domain.query.get(id)
    db.session.delete(domain)
    db.session.commit()
    
    data = {}
    return jsonify(data)
