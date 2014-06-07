# -*- coding: utf-8 -*-
__all__ = ['account_blueprint', 'login_manager']

import os
import sys
import json
import base64
import hashlib
from datetime import datetime, timedelta

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
from flask.ext.login import (
    current_user, login_required, fresh_login_required,
    login_user, logout_user, confirm_login,
    LoginManager, UserMixin,
)

# flask-wtf
from flask.ext.wtf import Form
from wtforms import validators
from wtforms import TextField, TextAreaField
from wtforms import PasswordField, SelectField, BooleanField
from wtforms_html5 import EmailField
from wtforms.fields.core import Field, UnboundField

# dateutil
from dateutil.parser import parse as dtparse

# config
from config.flask import FlaskConfig

# model
from model.db import db
from model.user import UserAccount

# flask mail
from mail import mail, Message

# login manager and blueprint
login_manager = LoginManager()
login_manager.login_view = FlaskConfig.LOGIN_VIEW
account_blueprint = Blueprint('account_blueprint', __name__)

# local in-process cache
# _users = {}

class User(UserMixin):
    def __new__(cls, username=None):
        # global _users
        # 
        # if username in _users:
        #    self = _users[username]
        #    return self
        
        if not UserAccount.query.filter_by(username=username).count():
            return None
        
        self = super(User, cls).__new__(cls)
        # _users[username] = self
        return self
    
    def __init__(self, username=None):
        # get user account from database
        if not UserAccount.query.filter_by(username=username).count():
            return
        
        # set flask user properties
        user_account = UserAccount.query.filter_by(username=username).one()
        
        for column in user_account.__table__.columns:
            v = getattr(user_account, column.name)
            setattr(self, column.name, v)
    
    def get_id(self):
        # NOTE: on purpose returns "username" but not "id"
        return self.username
    
    def is_active(self):
        return self.active
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True
    
    @classmethod
    def create_user(cls, **kwargs):
        # create UserAccount record
        user_account = UserAccount(**kwargs)
        db.session.add(user_account)
        db.session.commit()
        return True
    
    @classmethod
    def update_user(cls, username, **kwargs):
        # get user account from database
        if not UserAccount.query.filter_by(username=username).count():
            return False
        
        user_account = UserAccount.query.filter_by(username=username).one()
        
        for k, v in kwargs.iteritems():
            setattr(user_account, k, v)
        
        db.session.commit()
        return True
    
    @classmethod
    def delete_user(cls, username):
        # get user account from database
        if not UserAccount.query.filter_by(username=username).count():
            return False
        
        user_account = UserAccount.query.filter_by(username=username).one()
        db.session.delete(user_account)
        db.session.commit()
        return True
    
    @classmethod
    def check_password(cls, username, password):
        # get user account from database
        if not UserAccount.query.filter_by(username=username).count():
            return False
            
        user_account = UserAccount.query.filter_by(username=username).one()
        return user_account.password == password
    
    @classmethod
    def check_username(cls, username):
        if not UserAccount.query.filter_by(username=username).count():
            return False
        
        return True

class SignUpForm(Form):
    username = TextField('username', [validators.Required()])
    password = PasswordField('password', [validators.Required()])
    confirm_password = PasswordField('confirm_password', [validators.Required()])
    email = EmailField('email', [validators.Required()])
    
    '''
    # default usertype = 'user'
    usertype = SelectField('usertype', [validators.Required()], choices = [
        ('user',  'User'),
        ('super', 'Superuser'),
    ])
    
    # default active = True
    active = BooleanField('active', [validators.Optional()])
    '''
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None
    
    def validate(self):
        rv = Form.validate(self)
        
        if not rv:
            # invalid information
            return False
        
        if User.check_username(self.username.data):
            # user already exists
            self.username.errors.append('User already exists')
            return False
        
        if self.password.data != self.confirm_password.data:
            # passwords did not match
            self.password.errors.append('Passwords did not match')
            return False
        
        # find all field values, and create user
        dct = {}
        
        for k in dir(self.__class__):
            v = getattr(self.__class__, k)
            
            if isinstance(v, (Field, UnboundField)):
                v = getattr(self, k)
                dct[k] = v.data
        
        dct['usertype'] = 'user'
        dct['active'] = True
        
        User.create_user(**dct)
        user = User(username=self.username.data)
        
        if user is None:
            # user could not create for some reason
            self.username.errors.append('Invalid username')
            return False
        
        self.user = user
        return True

class SignInForm(Form):
    username = TextField('username', [validators.Required()])
    password = PasswordField('password', [validators.Required()])
    remember = BooleanField('remember')
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None
    
    def validate(self):
        rv = Form.validate(self)
        username = self.username.data
        password = self.password.data
        
        if not rv:
            # invalid information
            return False
        
        if not User.check_username(username):
            # user does NOT exist
            self.username.errors.append('Invalid username and/or password')
            return False
        
        if not User.check_password(username, password):
            # incorrect password
            self.password.errors.append('Invalid username and/or password')
            return False
        
        user = User(username=username)
        
        if user is None:
            # user could not create for some reason
            self.username.errors.append('Invalid username and/or password')
            return False
        
        self.user = user
        return True

@login_manager.user_loader
def load_user(username):
    user = User(username=username)
    # print 'load_user locals:', dict(locals())
    return user

@account_blueprint.route('/account/signup', methods=['GET', 'POST'])
def account_signup():
    error = None
    form = SignUpForm()
    print 'account_signup:', locals()

    if request.method == 'GET':
        next = request.args.get('next', '').replace('&amp;', '&')
        
        return render_template(
            'account-signup.html',
            form = form,
            error = error,
            next = next,
        )
    elif request.method == 'POST':
        # next or market selection
        next = request.form.get('next', url_for(FlaskConfig.DEFAULT_VIEW)).replace('&amp;', '&')
        
        if form.validate_on_submit():
            login_user(form.user)
            return redirect(next or url_for(FlaskConfig.DEFAULT_VIEW))

        return render_template(
            'account-signup.html',
            form = form,
            error = error,
            next = next,
        )

@account_blueprint.route('/account/signin', methods=['GET', 'POST'])
def account_signin():
    error = None
    form = SignInForm()
    print 'account_signin:', locals()
    
    if request.method == 'GET':
        next = request.args.get('next', '').replace('&amp;', '&')
        
        return render_template(
            'account-signin.html',
            form = form,
            error = error,
            next = next,
        )
    elif request.method == 'POST':
        # next
        next = ''
        
        if form.validate_on_submit():
            remember = form.remember.data if hasattr(form, 'remember') else False
            login_user(form.user, remember=remember)
            return redirect(next or url_for(FlaskConfig.DEFAULT_VIEW))
        
        return render_template(
            'account-signin.html',
            form = form,
            error = error,
            next = next,
        )

@account_blueprint.route('/account/signout', methods=['GET'])
@login_required
def account_signout():
    username = current_user.username
    print 'account_signout:', locals()
    
    # flask-login: logout user
    logout_user()
    return redirect(url_for(FlaskConfig.LOGIN_VIEW))

@account_blueprint.route('/account/recovery', methods=['GET'])
def account_recovery(username=None, uuid=None):
    print 'account_recovery locals:', dict(locals())
    
    # FIXME: implement
    return render_template(
        'account-recovery.html',
    )

#
# user profile
#
class UserForm(Form):
    username = TextField('username', [validators.Required()])
    current_password = PasswordField('current_password', [validators.Optional()])
    password = PasswordField('password', [validators.Optional()])
    confirm_password = PasswordField('confirm_password', [validators.Optional()])
    email = EmailField('email', [validators.Required()])
    
    usertype = SelectField('usertype', [validators.Optional()], choices = [
        ('user',  'User'),
        ('super', 'Superuser'),
    ])
    
    active = BooleanField('active', [validators.Optional()])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None
    
    def validate(self):
        rv = Form.validate(self)
        
        if not rv:
            # invalid information
            return False
        
        # get user account
        username = self.username.data
        
        if not UserAccount.query.filter_by(username=username).count():
            return False
        
        user_account = UserAccount.query.filter_by(username=username).one()
        
        # check password
        if self.current_password.data or self.password.data or self.confirm_password.data:
            if not User.check_password(self.username.data, self.current_password.data):
                # old password did not match
                self.current_password.errors.append('Current password did not match')
                return False

            if self.password.data != self.confirm_password.data:
                # passwords did not match
                self.password.errors.append('Passwords did not match')
                return False
        else:
            self.password.data = user_account.password
        
        # find all field values, and create user
        dct = {}
        
        for k in dir(self.__class__):
            v = getattr(self.__class__, k)
            
            if isinstance(v, (Field, UnboundField)):
                v = getattr(self, k)
                dct[k] = v.data
        
        # print '!!!', dct
        
        User.update_user(**dct)
        user = User(username=self.username.data)
        
        if user is None:
            # user could not be created for some reason
            self.username.errors.append('Invalid username')
            return False
        
        self.user = user
        return True

@account_blueprint.route('/account/profile', methods=['GET', 'POST'])
@login_required
def account_profile():
    username = current_user.username
    usertype = current_user.usertype
    print 'account_profile:', locals()
    
    if request.method == 'GET':
        if usertype == 'user':
            return redirect(url_for('account_blueprint.account_profile_user'))
        elif usertype == 'super':
            return redirect(url_for('account_blueprint.account_profile_super'))
        else:
            raise Exception(usertype)
    elif request.method == 'POST':
        # get user account properties
        user_account = UserAccount.query.filter_by(username=username).one()
        dct = {}
        
        for column in user_account.__table__.columns:
            v = getattr(user_account, column.name)
            dct[column.name] = v
        
        data = {
            'user_account': dct,
        }
        
        return jsonify(data)

@account_blueprint.route('/account/profile/user', methods=['GET', 'POST'])
@login_required
def account_profile_user():
    error = None
    form = UserForm()
    username = current_user.username
    print 'account_profile_user:', locals()
    
    if request.method == 'GET':
        # find all field values
        dct = {}
        user_account = UserAccount.query.filter_by(username=username).one()
        
        for column in user_account.__table__.columns:
            if column.name == 'id': continue
            v = getattr(user_account, column.name)
            
            if v:
                field = getattr(form, column.name)
                setattr(field, 'data', v)
            else:
                v = ''
            
            dct[column.name] = v
        
        return render_template(
            'account-profile-user.html',
            form = form,
            error = error,
            **dct
        )
    elif request.method == 'POST':
        # find all field values
        dct = {}
        user_account = UserAccount.query.filter_by(username=username).one()
        
        for k in dir(form):
            v = getattr(form, k)
            
            if isinstance(v, (Field, UnboundField)):
                field = getattr(form, k)
                v = field.data
                
                if v is None:
                    v = getattr(user_account, k)
                    field = getattr(form, k)
                    setattr(field, 'data', v)
                
                dct[k] = v
        
        if form.validate_on_submit():
            login_user(form.user)
        
        return render_template(
            'account-profile-user.html',
            form = form,
            error = error,
            **dct
        )

@account_blueprint.route('/account/profile/super', methods=['GET', 'POST'])
@login_required
def account_profile_super():
    error = None
    form = UserForm()
    username = current_user.username
    print 'account_profile_super:', locals()
    
    if request.method == 'GET':
        # find all field values
        dct = {}
        user_account = UserAccount.query.filter_by(username=username).one()
        
        for column in user_account.__table__.columns:
            if column.name == 'id': continue
            v = getattr(user_account, column.name)
            
            if v:
                field = getattr(form, column.name)
                setattr(field, 'data', v)
            else:
                v = ''
            
            dct[column.name] = v
        
        return render_template(
            'account-profile-super.html',
            form = form,
            error = error,
            **dct
        )
    elif request.method == 'POST':
        # find all field values
        dct = {}
        user_account = UserAccount.query.filter_by(username=username).one()
        
        for k in dir(form):
            v = getattr(form, k)
            
            if isinstance(v, (Field, UnboundField)):
                field = getattr(form, k)
                v = field.data
                
                if v is None:
                    v = getattr(user_account, k)
                    field = getattr(form, k)
                    setattr(field, 'data', v)
                
                dct[k] = v
        
        if form.validate_on_submit():
            login_user(form.user)
        
        return render_template(
            'account-profile-super.html',
            form = form,
            error = error,
            **dct
        )

#
# users
#
@account_blueprint.route('/account/users', methods=['GET'])
@login_required
def account_users():
    username = current_user.username
    print 'account_users:', locals()
    
    # get user account properties
    user_account = UserAccount.query.filter_by(username=username).one()
    dct = {}
    
    for column in user_account.__table__.columns:
        if column.name == 'id': continue
        v = getattr(user_account, column.name)
        dct[column.name] = v
    
    return render_template(
        'account-users.html',
        **dct
    )

@account_blueprint.route('/account/users/list', methods=['POST'])
@login_required
def account_users_list():
    username = current_user.username
    usertype = current_user.usertype
    print 'account_users_list locals:', dict(locals())
    
    # get all results
    results = []
    
    for user_account in UserAccount.query.all():
        result = {}
        
        for column in user_account.__table__.columns:
            v = getattr(user_account, column.name)
            result[column.name] = v
        
        results.append(result)
    
    data = {
        'results': results,
    }
    
    return jsonify(data)

@account_blueprint.route('/account/users/activate', methods=['POST'])
@login_required
def account_users_activate():
    username = current_user.username
    result = request.json['result']
    print 'account_users_activate locals:', dict(locals())
    
    # get user account properties
    user_account = UserAccount.query.filter_by(username=result['username']).one()
    user_account.active = True
    db.session.commit()
    result['active'] = True
    
    data = {
        'result': result,
    }
    
    return jsonify(data)

@account_blueprint.route('/account/users/deactivate', methods=['POST'])
@login_required
def account_users_deactivate():
    username = current_user.username
    result = request.json['result']
    print 'account_users_deactivate locals:', dict(locals())
    
    # get user account properties
    user_account = UserAccount.query.filter_by(username=result['username']).one()
    user_account.active = False
    db.session.commit()
    result['active'] = False
    
    data = {
        'result': result,
    }
    
    return jsonify(data)