# -*- coding: utf-8 -*-
__all__ = ['volume_blueprint']
import uuid
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
    
    if host_id is None and if mount_point_id is None:
        pass
    elif host_id is not None and mount_point_id is None:
        mount_points = MountPoint.query.filter_by(host_id=host_id).all()
        
        
    
    _volume['created'] = _volume['updated'] = datetime.utcnow()
    _volume['perm_name'] = '%s_%s' % (_volume['username'], uuid.uuid4().hex)
    
    volume = Volume(**_volume)
    db.session.add(volume)
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
    
    volume = Volume.query.get(id)
    db.session.delete(volume)
    db.session.commit()
    
    data = {}
    return jsonify(data)
