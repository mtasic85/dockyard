"use strict";

/*
 * host
 */
var host = {};

$.extend(host, {
    table: null,
    
    list: function(options) {
        options = options || {};
        
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
                host._add(host_);
            });
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
        });
    },
    
    _add: function(host_) {
        var tbody = host.table.find('tbody');
        var tr_template = _.template($('#table-row-host').html());
        var edit_template = _.template($('#modal-edit-host').html());
        
        var tr = $(tr_template(host_))
            .appendTo(tbody);
        
        // edit
        tr.find('a#edit').click(function(e) {
            var modal_div = $(edit_template(host_));
            
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
                
                // update host
                var _host = {
                    id: host_.id,
                    name: modal_div.find('#name').val(),
                    host: modal_div.find('#host').val(),
                    port: modal_div.find('#port').val(),
                    auth_username: modal_div.find('#auth_username').val(),
                    auth_password: modal_div.find('#auth_password').val(),
                };
                
                $.ajax({
                    type: 'POST',
                    url: '/host/update',
                    contentType: 'application/json;charset=utf-8',
                    dataType: 'json',
                    data: JSON.stringify({
                        host: _host,
                    }),
                })
                .done(function(data) {
                    // required to fix variable "host" from closure
                    _.each(_host, function(value, key) { host_[key] = value; });
                    
                    // update UI
                    host._update(data.host);
                    $.bootstrapGrowl('Host successfully updated.', {type: 'success', align: 'center'});
                })
                .error(function (xhr, ajaxOptions, thrownError) {
                    $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
                });
            });
            
            modal_div.modal({
                backdrop: 'static',
            });
        });
        
        // activate
        tr.find('a#activate').click(function(e) {
            // update host
            var _host = {
                id: host_.id,
                active: true,
            };
            
            $.ajax({
                type: 'POST',
                url: '/host/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    host: _host,
                }),
            })
            .done(function(data) {
                // required to fix variable "host" from closure
                _.each(_host, function(value, key) { host_[key] = value; });
                
                // update UI
                host._update(data.host);
                $.bootstrapGrowl('Host activated.', {type: 'success', align: 'center'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
        
        // deactivate
        tr.find('a#deactivate').click(function(e) {
            // update host
            var _host = {
                id: host_.id,
                active: false,
            };
            
            $.ajax({
                type: 'POST',
                url: '/host/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    host: _host,
                }),
            })
            .done(function(data) {
                // required to fix variable "host" from closure
                _.each(_host, function(value, key) { host_[key] = value; });
                
                // update UI
                host._update(data.host);
                $.bootstrapGrowl('Host deactivated.', {type: 'success', align: 'center'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
        
        // remove
        tr.find('a#remove').click(function(e) {
            $.ajax({
                type: 'POST',
                url: '/host/remove',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    id: host_.id,
                }),
            })
            .done(function(data) {
                tr.remove();
                $.bootstrapGrowl('Host successfully removed.', {type: 'success', align: 'center'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
    },
    
    add: function(options) {
        options = options || {};
        var new_template = _.template($('#modal-new-host').html());
        var modal_div = $(new_template());
        
        // host-switch
        modal_div.find('button#host-switch').click(function(e) {
            var isSelect = modal_div.find('select#host_id').length > 0;
            console.log(isSelect);
            
            if (isSelect) {
                var input = $('<input>')
                    .addClass('form-control')
                    .prop('id', 'host_id');
                
                modal_div.find('select#host_id').replaceWith(input);
            } else {
                var select = $('<select>')
                    .addClass('form-control')
                    .prop('id', 'host_id');
                
                modal_div.find('input#host_id').replaceWith(select);
            }
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
            
            // create host
            var _host = {
                name: modal_div.find('#name').val(),
                host: modal_div.find('#host').val(),
                port: modal_div.find('#port').val(),
                auth_username: modal_div.find('#auth_username').val(),
                auth_password: modal_div.find('#auth_password').val(),
            };
            
            $.ajax({
                type: 'POST',
                url: '/host/create',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    host: _host,
                }),
            })
            .done(function(data) {
                if (data.host !== undefined) {
                    // add single host
                    host._add(data.host);
                    $.bootstrapGrowl('Host successfully created.', {type: 'success', align: 'center'});
                } else if (data.hosts !== undefined) {
                    // add multiple hosts
                    _.each(data.hosts, function(_host) {
                        host._add(_host);
                    });
                    
                    $.bootstrapGrowl('Multiple Hosts successfully created.', {type: 'success', align: 'center'});
                }
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
        
        modal_div.modal({
            backdrop: 'static',
        });
    },
    
    _update: function(host_) {
        var tr = $('tr[data-id="' + host_.id + '"]');
        
        _.each(host_, function(value, key) {
            if (key === 'id') return;
            var td = tr.find('td#' + key);
            td.text(value);
        });
    },
});
