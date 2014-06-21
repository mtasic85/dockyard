# -*- coding: utf-8 -*-
__all__ = ['mount_blueprint']
import re
from itertools import product
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
from model.host import Host
from model.mount import MountPoint

mount_blueprint = Blueprint('mount_blueprint', __name__)

@mount_blueprint.route('/mount/points', methods=['GET'])
@login_required
def mount_points():
    username = current_user.username
    print 'mount_points:', locals()
    
    # get user account properties
    user_account = UserAccount.query.filter_by(username=username).one()
    dct = object_to_dict(user_account)
    
    return render_template(
        'mount-points.html',
        **dct
    )

@mount_blueprint.route('/mount/points/all', methods=['POST'])
@login_required
def mount_points_all():
    username = current_user.username
    usertype = current_user.usertype
    print 'mount_points_all:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    mounts = MountPoint.query.all()
    _mounts = objects_to_list(mounts)
    
    # insert host_name
    for _mount in _mounts:
        host = Host.query.get(_mount['host_id'])
        _mount['host_name'] = host.name
    
    data = {
        'mounts': _mounts,
    }
    
    return jsonify(data)

@mount_blueprint.route('/mount/point/create', methods=['POST'])
@login_required
def mount_create():
    username = current_user.username
    usertype = current_user.usertype
    _mount = request.json['mount']
    print 'mount_add:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    # try to find range patterns
    if 'host' in _mount:
        host = _mount['host']
        ranges = list(re.findall('\[\w+\-\w+\]', host))
    else:
        ranges = None
    
    if ranges:
        # generate all combinations
        patterns = ranges
        ranges = [range.strip('[]').split('-') for range in ranges]
        
        for i, r in enumerate(ranges):
            s, e = r
            
            if s.isdigit() and e.isdigit():
                s, e = map(int, r)
                r = range(s, e + 1)
                ranges[i] = r
            else:
                # FIXME: support alpha-num ranges for multi-character strings
                #        with same size
                assert len(s) == len(e) == 1
                s, e = map(ord, r)
                r = range(s, e + 1)
                r = map(chr, r)
                r = ''.join(r)
                ranges[i] = r
        
        combs = product(*ranges)
        
        # generate mount points
        name = _mount['name']
        device = _mount['device']
        mountpoint = _mount['mountpoint']
        filesystem = _mount['filesystem']
        capacity = _mount['capacity']
        
        for comb in combs:
            _host_id = host
            _name = name
            _device = device
            _mountpoint = mountpoint
            _capacity = capacity
            
            for p, c in zip(patterns, comb):
                _host_id = _host_id.replace(p, c)
                _name = _name.replace(p, c)
                _device = _device.replace(p, c)
                _mountpoint = _mountpoint.replace(p, c)
                _capacity = _capacity.replace(p, c)
                
                __mount = {
                    'host_id': _host_id,
                    'name': _name,
                    'device': _device,
                    'mountpoint': _mountpoint,
                    'capacity': _capacity,
                }
                
                print __mount
            
            data = {
            }
    else:
        mount = MountPoint(**_mount)
        _mount['created'] = _mount['updated'] = datetime.utcnow()
        db.session.add(mount)
        db.session.commit()
    
        _mount = object_to_dict(mount)
        
        # insert host_name
        host = Host.query.get(_mount['host_id'])
        _mount['host_name'] = host.name
        
        data = {
            'mount': _mount,
        }
    
    return jsonify(data)

@mount_blueprint.route('/mount/point/update', methods=['POST'])
@login_required
def mount_update():
    username = current_user.username
    usertype = current_user.usertype
    _mount = request.json['mount']
    print 'mount_update:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    mount = MountPoint.query.get(_mount['id'])
    _mount['updated'] = datetime.utcnow()
    update_object_with_dict(mount, _mount)
    db.session.commit()
    
    _mount = object_to_dict(mount)
    
    # insert host_name
    host = Host.query.get(_mount['host_id'])
    _mount['host_name'] = host.name
    
    data = {
        'mount': _mount,
    }
    
    return jsonify(data)

@mount_blueprint.route('/mount/point/remove', methods=['POST'])
@login_required
def mount_remove():
    username = current_user.username
    usertype = current_user.usertype
    id = request.json['id']
    print 'mount_remove:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    mount = MountPoint.query.get(id)
    db.session.delete(mount)
    db.session.commit()
    
    data = {}
    return jsonify(data)
