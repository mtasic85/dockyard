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
    
    # unpack
    _host_id = _container.get('host_id', None)
    _name = _container['name']
    _image_id = _container['image_id']
    _command = _container['command']
    _volumes = _container.get('volumes', [])
    _volumes_from = _container.get('volumes_from', [])
    _env_vars = _container['env_vars']
    _expose_ports = _container['expose_ports']
    _publish_ports = _container['publish_ports']
    _link_containers = _container.get('link_containers', [])
    _ram_limit = _container['ram_limit']
    _n_cpu_cores = _container['n_cpu_cores']
    
    # find suitable volume according to host
    if not _host_id and not _volumes:
        hosts = Host.query.all()
        host = random.choice(hosts)
        _host_id = host.id
        _host_host = host.host
        _volume_names = []
    elif not _host_id and _volumes:
        assert len(_volumes) == 1
        _volume_id = _volumes[0]
        volume = Volume.query.get(_volume_id)
        _volume_names = [volume.perm_name]
        
        host = Host.query.get(volume.host_id)
        _host_id = host.id
        _host_host = host.host
    else:
        host = Host.query.get(_host_id)
        _host_host = host.host
        _volume_names = []
    
    # find image name
    image = Image.query.get(_image_id)
    _image_name = image.name
    
    _volumes = json.dumps(_volumes)
    _volumes_from = json.dumps(_volumes_from)
    _link_containers = json.dumps(_link_containers)
    
    ##
    # create docker container
    url = 'http://%s:%i/containers/create' % (host.host, host.port)
    
    data_ = json.dumps({
        "Hostname": _host_host,
        "User": "",
        "Memory": _ram_limit,
        "MemorySwap": 0,
        "AttachStdin": True,
        "AttachStdout": True,
        "AttachStderr": True,
        "PortSpecs": None,
        "Tty": False,
        "OpenStdin": False,
        "StdinOnce": False,
        "Env": _env_vars,
        "Cmd": [_command],
        "Image": _image_name,
        "Volumes": {v: {} for v in _volume_names},
        "WorkingDir": "",
        "DisableNetwork": False,
        "ExposedPorts": {p: {} for p in _publish_ports.strip().split(',')},
    })
    
    print data_
    
    headers = {
        'content-type': 'application/json',
    }
    
    auth = HTTPBasicAuth(host.auth_username, host.auth_password)
    r = requests.post(url, data=data_, headers=headers, auth=auth)
    print r
    assert r.status_code == 200
    container_id = r.json()['Id']
    ##
    
    # insert container into database
    _status = 'ready'
    
    __container = {
        'host_id': _host_id,
        'name': _name,
        'image_id': _image_id,
        'command': _command,
        'volumes': _volumes,
        'volumes_from': _volumes_from,
        'env_vars': _env_vars,
        'expose_ports': _expose_ports,
        'publish_ports': _publish_ports,
        'link_containers': _link_containers,
        'ram_limit': _ram_limit,
        'n_cpu_cores': _n_cpu_cores,
        'cpu_share': _cpu_share,
        'status': _status,
    }
    
    __container['username'] = username
    __container['container_id'] = container_id
    __container['created'] = __container['updated'] = datetime.utcnow()
    
    __container['perm_name'] = '%s_%s' % (
        __container['username'],
        __container['name'],
    )
    
    container = Container(**__container)
    db.session.add(container)
    db.session.commit()
    
    __container = object_to_dict(container)
    
    # insert host_name
    host = Host.query.get(__container['host_id'])
    __container['host_name'] = host.name if host else 'ALL'
    
    # insert image_name
    image = Image.query.get(__container['image_id'])
    __container['image_name'] = image.name
    
    data = {
        'container': __container,
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
