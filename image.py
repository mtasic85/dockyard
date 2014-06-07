# -*- coding: utf-8 -*-
__all__ = ['image_blueprint']

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
from model.user import UserAccount

image_blueprint = Blueprint('image_blueprint', __name__)

@template_blueprint.route('/image/images', methods=['GET'])
@login_required
def image_images():
    username = current_user.username
    print 'image_images:', locals()
    
    # get user account properties
    user_account = UserAccount.query.filter_by(username=username).one()
    dct = {}
    
    for column in user_account.__table__.columns:
        v = getattr(user_account, column.name)
        dct[column.name] = v
    
    return render_template(
        'image-images.html',
        **dct
    )
