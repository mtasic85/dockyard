# -*- coding: utf-8 -*-
__all__ = ['container_blueprint']

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

container_blueprint = Blueprint('container_blueprint', __name__)

@container_blueprint.route('/container/containers', methods=['GET'])
@login_required
def container_containers():
    username = current_user.username
    print 'container_containers:', locals()
    
    # get user account properties
    user_account = UserAccount.query.filter_by(username=username).one()
    dct = {}
    
    for column in user_account.__table__.columns:
        v = getattr(user_account, column.name)
        dct[column.name] = v
    
    return render_template(
        'container-containers.html',
        **dct
    )
