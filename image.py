# -*- coding: utf-8 -*-
__all__ = ['image_blueprint']
import os
import sys
import json
import uuid
import random
from threading import Thread
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

image_blueprint = Blueprint('image_blueprint', __name__)

@image_blueprint.route('/images', methods=['GET'])
@login_required
def image_images():
    username = current_user.username
    print 'image_images:', locals()
    
    # get user account properties
    user_account = UserAccount.query.filter_by(username=username).one()
    dct = object_to_dict(user_account)
    
    return render_template(
        'image-images.html',
        **dct
    )

@image_blueprint.route('/images/all', methods=['POST'])
@login_required
def image_images_all():
    username = current_user.username
    usertype = current_user.usertype
    print 'image_images_all:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    images = Image.query.all()
    _images = objects_to_list(images)
    
    # insert host_name
    for _image in _images:
        host = Host.query.get(_image['host_id'])
        
        if host:
            _image['host_name'] = host.name
        else:
            _image['host_name'] = 'ALL'
    
    data = {
        'images': _images,
    }
    
    return jsonify(data)

@image_blueprint.route('/image/create', methods=['POST'])
@login_required
def image_create():
    username = current_user.username
    usertype = current_user.usertype
    _image = request.json['image']
    print 'image_add:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    _image['status'] = 'downloading'
    _image['created'] = _image['updated'] = datetime.utcnow()
    image = Image(**_image)
    db.session.add(image)
    
    ##
    # "async" create/pull image
    def _requests_post(*args, **kwargs):
        try:
            r = requests.post(*args, **kwargs)
            assert r.status_code == 200
            print r
        except requests.exceptions.ChunkedEncodingError as e:
            print e
    
    def _image_create():
        # get all hosts
        hosts = Host.query.all()
        threads = []
        
        for host in hosts:
            # create volume at host
            url = 'http://%s:%i/docker/images/create?fromImage=%s' % (
                host.host,
                host.port,
                _image['name'],
            )
            
            data_ = json.dumps({})
            headers = {'content-type': 'application/json'}
            auth = auth=HTTPBasicAuth(host.auth_username, host.auth_password)
            
            t = Thread(
                target = _requests_post,
                args = (url,),
                kwargs = dict(data=data_, headers=headers, auth=auth)
            )
            
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        image.status = 'ready'
        db.session.commit()
        print '!!!', 'DONE'
    
    t = Thread(target=_image_create)
    t.start()
    ##
    
    '''
    ##
    # get all hosts
    hosts = Host.query.all()
    
    for host in hosts:
        # create volume at host
        url = 'http://%s:%i/images/create?fromImage=%s' % (
            host.host,
            host.port,
            _image['name'],
        )
        
        data_ = json.dumps({})
        headers = {'content-type': 'application/json'}
        auth = auth=HTTPBasicAuth(host.auth_username, host.auth_password)
        
        try:
            r = requests.post(url, data=data_, headers=headers, auth=auth)
            print r
        except requests.exceptions.ChunkedEncodingError as e:
            print e
    
    image.status = 'ready'
    ##
    '''
    
    db.session.commit()
    _image = object_to_dict(image)
    
    # insert host_name
    host = Host.query.get(_image['host_id'])
    
    if host:
        _image['host_name'] = host.name
    else:
        _image['host_name'] = 'ALL'
    
    data = {
        'image': _image,
    }
    
    return jsonify(data)

@image_blueprint.route('/image/update', methods=['POST'])
@login_required
def image_update():
    username = current_user.username
    usertype = current_user.usertype
    _image = request.json['image']
    print 'image_update:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    image = Image.query.get(_image['id'])
    _image['updated'] = datetime.utcnow()
    update_object_with_dict(image, _image)
    db.session.commit()
    
    _image = object_to_dict(image)
    
    # insert host_name
    host = Host.query.get(_image['host_id'])
    assert host is not None
    _image['host_name'] = host.name
    
    data = {
        'image': _image,
    }
    
    return jsonify(data)

@image_blueprint.route('/image/remove', methods=['POST'])
@login_required
def image_remove():
    username = current_user.username
    usertype = current_user.usertype
    id = request.json['id']
    print 'image_remove:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    image = Image.query.get(id)
    db.session.delete(image)
    db.session.commit()
    
    data = {}
    return jsonify(data)
