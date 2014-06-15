"use strict";

/*
 * route
 */
var route = {};

$.extend(route, {
    table: null,
    domain_id: null,
    
    list: function(options) {
        options = options || {};
        
        $.ajax({
            type: 'POST',
            url: '/network/routes/all',
            contentType: 'application/json;charset=utf-8',
            dataType: 'json',
            data: JSON.stringify({}),
        })
        .done(function(data) {
            // console.log(data);
            _.each(data.routes, function(route_) {
                route._add(route_);
            });
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
        });
    },
    
    _add: function(route_) {
        var tbody = route.table.find('tbody');
        var tr_template = _.template($('#table-row-route').html());
        var edit_template = _.template($('#modal-edit-route').html());
        
        var tr = $(tr_template(route_))
            .appendTo(tbody);
        
        // edit
        tr.find('a#edit').click(function(e) {
            var modal_div = $(edit_template(route_));
            var host_id_select = modal_div.find('#host_id');
            
            // populate hosts
            $.ajax({
                type: 'POST',
                url: '/hosts/all',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({}),
            })
            .done(function(data) {
                // console.log(data);
                _.each(data.hosts, function(host_) {
                    var option = $('<option>')
                        .attr('value', host_.id)
                        .text(host_.name)
                        .appendTo(host_id_select);
                });
                
                // select host
                host_id_select.val(route_.host_id);
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
            
            // close
            modal_div.find('button#close').click(function(e) {
                // close modal
                modal_div.modal('hide');
                setTimeout(function() { modal_div.remove();}, 500);
                $('.modal-backdrop').remove();
            });
            
            // update
            modal_div.find('button#update').click(function(e) {
                // close modal
                modal_div.modal('hide');
                setTimeout(function() { modal_div.remove();}, 500);
                $('.modal-backdrop').remove();
                
                // update route
                var _route = {
                    id: route_.id,
                    domain_id: modal_div.find('#domain_id').val(),
                    host_id: modal_div.find('#host_id').val(),
                    host_port: modal_div.find('#host_port').val(),
                    conatiner_id: modal_div.find('#conatiner_id').val(),
                    conatiner_port: modal_div.find('#conatiner_port').val(),
                    username: modal_div.find('#username').val(),
                };
                
                $.ajax({
                    type: 'POST',
                    url: '/network/route/update',
                    contentType: 'application/json;charset=utf-8',
                    dataType: 'json',
                    data: JSON.stringify({
                        route: _route,
                    }),
                })
                .done(function(data) {
                    // required to fix variable "route" from closure
                    _.each(_route, function(value, key) { route_[key] = value; });
                    
                    // update UI
                    route._update(data.route);
                    $.bootstrapGrowl('Route successfully updated.', {type: 'success'});
                })
                .error(function (xhr, ajaxOptions, thrownError) {
                    $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
                });
            });
            
            modal_div.modal({
                backdrop: 'static',
            });
        });
        
        // activate
        tr.find('a#activate').click(function(e) {
            // update route
            var _route = {
                id: route_.id,
                active: true,
            };
            
            $.ajax({
                type: 'POST',
                url: '/network/route/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    route: _route,
                }),
            })
            .done(function(data) {
                // required to fix variable "route" from closure
                _.each(_route, function(value, key) { route_[key] = value; });
                
                // update UI
                route._update(data.route);
                $.bootstrapGrowl('Route activated.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        // deactivate
        tr.find('a#deactivate').click(function(e) {
            // update route
            var _route = {
                id: route_.id,
                active: false,
            };
            
            $.ajax({
                type: 'POST',
                url: '/network/route/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    route: _route,
                }),
            })
            .done(function(data) {
                // required to fix variable "route" from closure
                _.each(_route, function(value, key) { route_[key] = value; });
                
                // update UI
                route._update(data.route);
                $.bootstrapGrowl('Route deactivated.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        // remove
        tr.find('a#remove').click(function(e) {
            $.ajax({
                type: 'POST',
                url: '/network/route/remove',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    id: route_.id,
                }),
            })
            .done(function(data) {
                tr.remove();
                $.bootstrapGrowl('Route successfully removed.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
    },
    
    add: function(options) {
        options = options || {};
        var new_template = _.template($('#modal-new-route').html());
        var modal_div = $(new_template());
        var host_id_select = modal_div.find('#host_id');
        
        // populate hosts
        $.ajax({
            type: 'POST',
            url: '/hosts/all',
            contentType: 'application/json;charset=utf-8',
            dataType: 'json',
            data: JSON.stringify({}),
        })
        .done(function(data) {
            // console.log(data);
            _.each(data.hosts, function(host_) {
                var option = $('<option>')
                    .attr('value', host_.id)
                    .text(host_.name)
                    .appendTo(host_id_select);
            });
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
        });
        
        // close
        modal_div.find('button#close').click(function(e) {
            // close modal
            modal_div.modal('hide');
            setTimeout(function() { modal_div.remove();}, 500);
            $('.modal-backdrop').remove();
        });
        
        // update
        modal_div.find('button#create').click(function(e) {
            // close modal
            modal_div.modal('hide');
            setTimeout(function() { modal_div.remove();}, 500);
            $('.modal-backdrop').remove();
            
            // create route
            var _route = {
                domain_id: modal_div.find('#domain_id').val(),
                host_id: modal_div.find('#host_id').val(),
                host_port: modal_div.find('#host_port').val(),
                conatiner_id: modal_div.find('#conatiner_id').val(),
                conatiner_port: modal_div.find('#conatiner_port').val(),
                username: modal_div.find('#username').val(),
            };
            
            $.ajax({
                type: 'POST',
                url: '/network/route/create',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    route: _route,
                }),
            })
            .done(function(data) {
                route._add(data.route);
                $.bootstrapGrowl('Route successfully created.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        modal_div.modal({
            backdrop: 'static',
        });
    },
    
    _update: function(route_) {
        var tr = $('tr[data-id="' + route_.id + '"]');
        
        _.each(route_, function(value, key) {
            if (key === 'id') return;
            var td = tr.find('td#' + key);
            td.text(value);
        });
    },
});

