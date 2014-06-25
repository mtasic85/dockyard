# -*- coding: utf-8 -*-
__all__ = ['container_blueprint']
import os
import sys
import json
import uuid
import random
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
from model.image import Image
from model.volume import Volume
from model.container import Container

container_blueprint = Blueprint('container_blueprint', __name__)

@container_blueprint.route('/containers', methods=['GET'])
@login_required
def container_containers():
    username = current_user.username
    print 'container_containers:', locals()
    
    # get user account properties
    user_account = UserAccount.query.filter_by(username=username).one()
    dct = object_to_dict(user_account)
    
    return render_template(
        'container-containers.html',
        **dct
    )

@container_blueprint.route('/containers/all', methods=['POST'])
@login_required
def container_containers_all():
    username = current_user.username
    usertype = current_user.usertype
    print 'container_containers_all:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    containers = Container.query.all()
    _containers = objects_to_list(containers)
    
    # insert host_name
    # insert image_name
    for _container in _containers:
        host = Host.query.get(_container['host_id'])
        # assert host is not None
        
        image = Image.query.get(_container['image_id'])
        assert image is not None
        
        _container['host_name'] = host.name if host else 'ALL'
        _container['image_name'] = image.name
    
    data = {
        'containers': _containers,
    }
    
    return jsonify(data)

@container_blueprint.route('/container/create', methods=['POST'])
@login_required
def container_create():
    username = current_user.username
    usertype = current_user.usertype
    _container = request.json['container']
    print 'container_add:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    host_id = _container.get('host_id', None)
    name = _container['name']
    image_id = _container['image_id']
    command = _container['command']
    volumes = _container.get('volumes', None)
    # volumes_from = _container.get('volumes_from', None)
    env_vars = _container['env_vars']
    expose_ports = _container['expose_ports']
    publish_ports = _container['publish_ports']
    # link_containers = _container['link_containers']
    ram_limit = _container['ram_limit']
    n_cpu_cores = _container['n_cpu_cores']
    
    if 
    _container['username'] = username
    _container['created'] = _container['updated'] = datetime.utcnow()
    _container['perm_name'] = '%s_%s' % (_container['username'], _container['name'])
    
    container = Container(**_container)
    db.session.add(container)
    db.session.commit()
    
    _container = object_to_dict(container)
    
    # insert host_name
    # insert image_name
    host = Host.query.get(_container['host_id'])
    # assert host is not None
    
    image = Image.query.get(_container['image_id'])
    assert image is not None
    
    _container['host_name'] = host.name if host else 'ALL'
    _container['image_name'] = image.name
    
    data = {
        'container': _container,
    }
    
    return jsonify(data)

@container_blueprint.route('/container/remove', methods=['POST'])
@login_required
def container_remove():
    username = current_user.username
    usertype = current_user.usertype
    id = request.json['id']
    print 'container_remove:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    container = Container.query.get(id)
    db.session.delete(container)
    db.session.commit()
    
    data = {}
    return jsonify(data)
