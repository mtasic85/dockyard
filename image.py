# -*- coding: utf-8 -*-
__all__ = ['image_blueprint']
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
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    images = Image.query.all()
    _images = objects_to_list(images)
    
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
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    image = Image(**_image)
    _image['created'] = _image['updated'] = datetime.utcnow()
    db.session.add(image)
    db.session.commit()
    
    _image = object_to_dict(image)
    
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
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    image = Image.query.get(_image['id'])
    _image['updated'] = datetime.utcnow()
    update_object_with_dict(image, _image)
    db.session.commit()
    
    _image = object_to_dict(image)
    
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
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    image = Image.query.get(id)
    db.session.delete(image)
    db.session.commit()
    
    data = {}
    return jsonify(data)
