# -*- coding: utf-8 -*-
__all__ = ['network_blueprint']
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
from model.container import Container
from model.network import Domain, Route

network_blueprint = Blueprint('network_blueprint', __name__)

#
# domain
#
@network_blueprint.route('/network/domains', methods=['GET'])
@login_required
def network_domains():
    username = current_user.username
    print 'network_domains:', locals()
    
    # get user account properties
    user_account = UserAccount.query.filter_by(username=username).one()
    dct = object_to_dict(user_account)
    
    return render_template(
        'network-domains.html',
        **dct
    )

@network_blueprint.route('/network/domains/all', methods=['POST'])
@login_required
def network_domains_all():
    username = current_user.username
    usertype = current_user.usertype
    print 'network_domains_all:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    domains = Domain.query.all()
    _domains = objects_to_list(domains)
    
    data = {
        'domains': _domains,
    }
    
    return jsonify(data)

@network_blueprint.route('/network/domain/create', methods=['POST'])
@login_required
def network_domain_create():
    username = current_user.username
    usertype = current_user.usertype
    _domain = request.json['domain']
    print 'network_domain_create:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    _domain['created'] = _domain['updated'] = datetime.utcnow()
    domain = Domain(**_domain)
    db.session.add(domain)
    db.session.commit()
    
    _domain = object_to_dict(domain)
    
    data = {
        'domain': _domain,
    }
    
    return jsonify(data)

@network_blueprint.route('/network/domain/update', methods=['POST'])
@login_required
def network_domain_update():
    username = current_user.username
    usertype = current_user.usertype
    _domain = request.json['domain']
    print 'network_domain_update:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    domain = Domain.query.get(_domain['id'])
    _domain['updated'] = datetime.utcnow()
    update_object_with_dict(domain, _domain)
    db.session.commit()
    
    _domain = object_to_dict(domain)
    
    data = {
        'domain': _domain,
    }
    
    return jsonify(data)

@network_blueprint.route('/network/domain/remove', methods=['POST'])
@login_required
def network_domain_remove():
    username = current_user.username
    usertype = current_user.usertype
    id = request.json['id']
    print 'network_domain_remove:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    domain = Domain.query.get(id)
    db.session.delete(domain)
    db.session.commit()
    
    data = {}
    return jsonify(data)

#
# route
#
@network_blueprint.route('/network/routes', methods=['GET'])
@network_blueprint.route('/network/routes/<int:domain_id>', methods=['GET'])
@login_required
def network_routes(domain_id=None):
    username = current_user.username
    print 'network_routes:', locals()
    
    # get user account properties
    user_account = UserAccount.query.filter_by(username=username).one()
    dct = object_to_dict(user_account)
    
    return render_template(
        'network-routes.html',
        domain_id = domain_id,
        **dct
    )

@network_blueprint.route('/network/routes/all', methods=['POST'])
@login_required
def network_routes_all():
    username = current_user.username
    usertype = current_user.usertype
    print 'network_routes_all:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    routes = Route.query.all()
    _routes = objects_to_list(routes)
    
    # insert domain, host, container names
    for _route in _routes:
        domain = Domain.query.get(_route['domain_id'])
        assert domain is not None
        
        host = Host.query.get(_route['host_id'])
        assert host is not None
        
        container = Container.query.get(_route['container_id'])
        assert container is not None
        
        _route['domain_domain'] = domain.domain
        _route['host_name'] = host.name
        _route['container_name'] = container.name
        _route['container_container_id'] = container.container_id
    
    data = {
        'routes': _routes,
    }
    
    return jsonify(data)

@network_blueprint.route('/network/route/create', methods=['POST'])
@login_required
def network_route_create():
    username = current_user.username
    usertype = current_user.usertype
    _route = request.json['route']
    print 'network_route_create:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    _route['created'] = _route['updated'] = datetime.utcnow()
    route = Route(**_route)
    db.session.add(route)
    db.session.commit()
    
    _route = object_to_dict(route)
    
    # insert domain, host, container name
    domain = Domain.query.get(_route['domain_id'])
    assert domain is not None
    
    host = Host.query.get(_route['host_id'])
    assert host is not None
    
    container = Container.query.get(_route['container_id'])
    assert container is not None
    
    _route['domain_domain'] = domain.domain
    _route['host_name'] = host.name
    _route['container_name'] = container.name
    _route['container_container_id'] = container.container_id
    
    data = {
        'route': _route,
    }
    
    return jsonify(data)

@network_blueprint.route('/network/route/update', methods=['POST'])
@login_required
def network_route_update():
    username = current_user.username
    usertype = current_user.usertype
    _route = request.json['route']
    print 'network_route_update:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
        
    route = Route.query.get(_route['id'])
    _route['updated'] = datetime.utcnow()
    update_object_with_dict(route, _route)
    db.session.commit()
    
    _route = object_to_dict(route)
    
    # insert domain, host, container name
    domain = Domain.query.get(_route['domain_id'])
    assert domain is not None
    
    host = Host.query.get(_route['host_id'])
    assert host is not None
    
    container = Container.query.get(_route['container_id'])
    assert container is not None
    
    _route['domain_domain'] = domain.domain
    _route['host_name'] = host.name
    _route['container_name'] = container.name
    _route['container_container_id'] = container.container_id
    
    data = {
        'route': _route,
    }
    
    return jsonify(data)

@network_blueprint.route('/network/route/remove', methods=['POST'])
@login_required
def network_route_remove():
    username = current_user.username
    usertype = current_user.usertype
    id = request.json['id']
    print 'network_route_remove:', locals()
    
    if usertype != 'super':
        data = {}
        return jsonify(data)
    
    route = Route.query.get(id)
    db.session.delete(route)
    db.session.commit()
    
    data = {}
    return jsonify(data)
