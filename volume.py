# -*- coding: utf-8 -*-
__all__ = ['volume_blueprint']
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

# model
from model.db import db
from model.db import object_to_dict, objects_to_list, update_object_with_dict
from model.user import UserAccount, UserQuota
from model.host import Host
from model.volume import Volume
from model.mount import MountPoint

volume_blueprint = Blueprint('volume_blueprint', __name__)

@volume_blueprint.route('/volumes', methods=['GET'])
@login_required
def volume_volumes():
    username = current_user.username
    print 'volume_volumes:', locals()
    
    # get user account properties
    user_account = UserAccount.query.filter_by(username=username).one()
    dct = object_to_dict(user_account)
    
    return render_template(
        'volume-volumes.html',
        **dct
    )

@volume_blueprint.route('/volumes/all', methods=['POST'])
@login_required
def volume_volumes_all():
    username = current_user.username
    usertype = current_user.usertype
    print 'volume_volumes_all:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    volumes = Volume.query.all()
    _volumes = objects_to_list(volumes)
    
    # insert host_name
    # insert mount_point_name
    for _volume in _volumes:
        host = Host.query.get(_volume['host_id'])
        assert host is not None
        
        mount_point = MountPoint.query.get(_volume['mount_point_id'])
        assert mount_point is not None
        
        _volume['host_name'] = host.name
        _volume['mount_point_name'] = mount_point.name
    
    data = {
        'volumes': _volumes,
    }
    
    return jsonify(data)

@volume_blueprint.route('/volume/create', methods=['POST'])
@login_required
def volume_create():
    username = current_user.username
    usertype = current_user.usertype
    _volume = request.json['volume']
    print 'volume_add:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    host_id = _volume.get('host_id', None)
    mount_point_id = _volume.get('mount_point_id', None)
    name = _volume['name']
    capacity = _volume['capacity']
    username_ = _volume['username']
    
    # find available host and/or mount point
    if host_id is None or mount_point_id is None:
        query = MountPoint.query
        
        if host_id is not None and mount_point_id is None:
            query = query.filter_by(host_id=host_id)
        
        mount_points = query.all()
        
        mount_points = [
            m for m in mount_points
            if m.capacity - m.reserved >= capacity
        ]
        
        # no mount_points available
        if not mount_points:
            data = {
                'error': 'The is no available space.'\
                         'Try smaller volume capacity than %s GB.' % capacity,
            }
            
            return jsonify(data)
        
        # take first available slice
        mount_points.sort(key=lambda m: m.capacity - m.reserved)
        mount_point = random.choice(mount_points)
        
        # host, mount_point
        host_id = mount_point.host_id
        mount_point_id = mount_point.id
    
    # host_name
    host = Host.query.get(host_id)
    assert host is not None
    
    # mount_point_name
    mount_point = MountPoint.query.get(mount_point_id)
    assert mount_point is not None
    
    # increase reserved storage at mount point
    mount_point.reserved = mount_point.reserved + capacity
    
    # insert volume into database
    __volume = {
        'host_id': host_id,
        'mount_point_id': mount_point_id,
        'name': name
        'capacity': capacity,
        'username': username_,
    }
    
    __volume['created'] = __volume['updated'] = datetime.utcnow()
    __volume['perm_name'] = '%s_%s' % (username_, uuid.uuid4().hex)
    
    volume = Volume(**__volume)
    db.session.add(volume)
    db.session.commit()
    
    # return response
    __volume = object_to_dict(volume)
    
    # insert host_name
    # insert mount_point_name
    __volume['host_name'] = host.name
    __volume['mount_point_name'] = mount_point.name
    
    data = {
        'volume': __volume,
    }
    
    return jsonify(data)

@volume_blueprint.route('/volume/update', methods=['POST'])
@login_required
def volume_update():
    username = current_user.username
    usertype = current_user.usertype
    _volume = request.json['volume']
    print 'volume_update:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    volume = Volume.query.get(_volume['id'])
    _volume['updated'] = datetime.utcnow()
    update_object_with_dict(volume, _volume)
    db.session.commit()
    
    _volume = object_to_dict(volume)
    
    # insert host_name
    # insert mount_point_name
    host = Host.query.get(_volume['host_id'])
    assert host is not None
    
    mount_point = MountPoint.query.get(_volume['mount_point_id'])
    assert mount_point is not None
    
    _volume['host_name'] = host.name
    _volume['mount_point_name'] = mount_point.name
    
    data = {
        'volume': _volume,
    }
    
    return jsonify(data)

@volume_blueprint.route('/volume/remove', methods=['POST'])
@login_required
def volume_remove():
    username = current_user.username
    usertype = current_user.usertype
    id = request.json['id']
    print 'volume_remove:', locals()
    
    # FIXME:
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    # volume
    volume = Volume.query.get(id)
    
    # host
    host = Host.query.get(_volume['host_id'])
    assert host is not None
    
    # mount point
    mount_point = MountPoint.query.get(_volume['mount_point_id'])
    assert mount_point is not None
    
    # decrease reserved sotrage at mount point
    mount_point.reserved = mount_point.reserved - volume.capacity
    
    # delete volume
    db.session.delete(volume)
    db.session.commit()
    
    data = {}
    return jsonify(data)
