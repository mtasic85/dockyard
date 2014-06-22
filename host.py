# -*- coding: utf-8 -*-
__all__ = ['host_blueprint']
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

# requests
import requests
from requests.auth import HTTPBasicAuth

# model
from model.db import db
from model.db import object_to_dict, objects_to_list, update_object_with_dict
from model.user import UserAccount, UserQuota
from model.host import Host

host_blueprint = Blueprint('host_blueprint', __name__)

@host_blueprint.route('/hosts', methods=['GET'])
@login_required
def host_hosts():
    username = current_user.username
    print 'host_hosts:', locals()
    
    # get user account properties
    user_account = UserAccount.query.filter_by(username=username).one()
    dct = object_to_dict(user_account)
    
    return render_template(
        'host-hosts.html',
        **dct
    )

@host_blueprint.route('/hosts/all', methods=['POST'])
@login_required
def host_hosts_all():
    username = current_user.username
    usertype = current_user.usertype
    print 'host_hosts_all:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    hosts = Host.query.all()
    _hosts = objects_to_list(hosts)
    
    data = {
        'hosts': _hosts,
    }
    
    return jsonify(data)

@host_blueprint.route('/host/create', methods=['POST'])
@login_required
def host_create():
    username = current_user.username
    usertype = current_user.usertype
    _host = request.json['host']
    print 'host_add:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    name = _host['name']
    host = _host['host']
    port = _host['port']
    auth_username = _host['auth_username']
    auth_password = _host['auth_password']
    ram_capacity = _host['ram_capacity']
    ram_reserved = _host['ram_reserved']
    
    if '[' in name and '-' in name and ']' in name and \
       '[' in host and '-' in host and ']' in host:
        _hosts = []
        hosts = []
        
        # name base/range
        s = name.find('[')
        e = name.find(']')
        name_base = name[:s]
        name_range = name[s + 1:e]
        name_range = name_range.strip(' ').strip()
        name_range = map(int, name_range.split('-'))
        name_range[1] += 1
        
        # host base/range
        s = host.find('[')
        e = host.find(']')
        host_base = host[:s]
        host_range = host[s + 1:e]
        host_range = host_range.strip(' ').strip()
        host_range = map(int, host_range.split('-'))
        host_range[1] += 1
        
        for i, j in zip(range(*name_range), range(*host_range)):
            __host = {
                'name': '%s%i' % (name_base, i),
                'host': '%s%i' % (host_base, j),
                'port': port,
                'auth_username': auth_username,
                'auth_password': auth_password,
                'ram_capacity': ram_capacity,
                'ram_reserved': ram_reserved,
            }
            
            __host['created'] = __host['updated'] = datetime.utcnow()
            host = Host(**__host)
            db.session.add(host)
            hosts.append(host)
        
        db.session.commit()
        
        for host in hosts:
            __host = object_to_dict(host)
            _hosts.append(__host)
        
        data = {
            'hosts': _hosts,
        }
    else:
        _host['created'] = _host['updated'] = datetime.utcnow()
        host = Host(**_host)
        db.session.add(host)
        db.session.commit()
        _host = object_to_dict(host)
        
        data = {
            'host': _host,
        }
    
    return jsonify(data)

@host_blueprint.route('/host/update', methods=['POST'])
@login_required
def host_update():
    username = current_user.username
    usertype = current_user.usertype
    _host = request.json['host']
    print 'host_update:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    host = Host.query.get(_host['id'])
    assert host is not None
    
    _host['updated'] = datetime.utcnow()
    update_object_with_dict(host, _host)
    db.session.commit()
    
    _host = object_to_dict(host)
    
    data = {
        'host': _host,
    }
    
    return jsonify(data)

@host_blueprint.route('/host/remove', methods=['POST'])
@login_required
def host_remove():
    username = current_user.username
    usertype = current_user.usertype
    id = request.json['id']
    print 'host_remove:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    host = Host.query.get(id)
    assert host is not None
    db.session.delete(host)
    db.session.commit()
    
    data = {}
    return jsonify(data)
