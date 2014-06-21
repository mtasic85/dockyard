"use strict";

/*
 * mount
 */
var mount = {};

$.extend(mount, {
    table: null,
    
    list: function(options) {
        options = options || {};
        
        $.ajax({
            type: 'POST',
            url: '/mount/points/all',
            contentType: 'application/json;charset=utf-8',
            dataType: 'json',
            data: JSON.stringify({}),
        })
        .done(function(data) {
            // console.log(data);
            _.each(data.mounts, function(mount_) {
                mount._add(mount_);
            });
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
        });
    },
    
    _add: function(mount_) {
        var tbody = mount.table.find('tbody');
        var tr_template = _.template($('#table-row-mount').html());
        var edit_template = _.template($('#modal-edit-mount').html());
        
        var tr = $(tr_template(mount_))
            .appendTo(tbody);
        
        // edit
        tr.find('a#edit').click(function(e) {
            var modal_div = $(edit_template(mount_));
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
                host_id_select.val(mount_.host_id);
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
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
                
                // update mount
                var _mount = {
                    id: mount_.id,
                    name: modal_div.find('#name').val(),
                    host_id: modal_div.find('#host_id').val(),
                    host: modal_div.find('#host').val(),
                    device: modal_div.find('#device').val(),
                    mountpoint: modal_div.find('#mountpoint').val(),
                    filesystem: modal_div.find('#filesystem').val(),
                    capacity: modal_div.find('#capacity').val(),
                };
                
                $.ajax({
                    type: 'POST',
                    url: '/mount/point/update',
                    contentType: 'application/json;charset=utf-8',
                    dataType: 'json',
                    data: JSON.stringify({
                        mount: _mount,
                    }),
                })
                .done(function(data) {
                    // required to fix variable "mount" from closure
                    _.each(_mount, function(value, key) { mount_[key] = value; });
                    
                    // update UI
                    mount._update(data.mount);
                    $.bootstrapGrowl('Mount Point successfully updated.', {type: 'success', align: 'center'});
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
            // update mount
            var _mount = {
                id: mount_.id,
                active: true,
            };
            
            $.ajax({
                type: 'POST',
                url: '/mount/point/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    mount: _mount,
                }),
            })
            .done(function(data) {
                // required to fix variable "mount" from closure
                _.each(_mount, function(value, key) { mount_[key] = value; });
                
                // update UI
                mount._update(data.mount);
                $.bootstrapGrowl('Mount Point activated.', {type: 'success', align: 'center'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
        
        // deactivate
        tr.find('a#deactivate').click(function(e) {
            // update mount
            var _mount = {
                id: mount_.id,
                active: false,
            };
            
            $.ajax({
                type: 'POST',
                url: '/mount/point/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    mount: _mount,
                }),
            })
            .done(function(data) {
                // required to fix variable "mount" from closure
                _.each(_mount, function(value, key) { mount_[key] = value; });
                
                // update UI
                mount._update(data.mount);
                $.bootstrapGrowl('Mount Point deactivated.', {type: 'success', align: 'center'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
        
        // remove
        tr.find('a#remove').click(function(e) {
            $.ajax({
                type: 'POST',
                url: '/mount/point/remove',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    id: mount_.id,
                }),
            })
            .done(function(data) {
                tr.remove();
                $.bootstrapGrowl('User successfully removed.', {type: 'success', align: 'center'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
    },
    
    _populate_hosts: function(host_id_select) {
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
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
        });
    },
    
    add: function(options) {
        options = options || {};
        var new_template = _.template($('#modal-new-mount').html());
        var modal_div = $(new_template());
        var host_id_select = modal_div.find('#host_id');
        
        // host-switch
        modal_div.find('button#host-switch').click(function(e) {
            var hostIsSelect = modal_div.find('select#host_id').length > 0;
            
            if (hostIsSelect) {
                var input = $('<input>')
                    .addClass('form-control')
                    .prop('id', 'host');
                
                modal_div.find('select#host_id')
                    .replaceWith(input);
            } else {
                var select = $('<select>')
                    .addClass('form-control')
                    .prop('id', 'host_id');
                
                modal_div.find('input#host')
                    .replaceWith(select);
                
                // populate hosts
                mount._populate_hosts(select);
            }
        });
        
        // populate hosts
        mount._populate_hosts(host_id_select);
        
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
            
            // create mount
            var _mount = {
                name: modal_div.find('#name').val(),
                host_id: modal_div.find('#host_id').val(),
                host: modal_div.find('#host').val(),
                device: modal_div.find('#device').val(),
                mountpoint: modal_div.find('#mountpoint').val(),
                filesystem: modal_div.find('#filesystem').val(),
                capacity: modal_div.find('#capacity').val(),
            };
            
            $.ajax({
                type: 'POST',
                url: '/mount/point/create',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    mount: _mount,
                }),
            })
            .done(function(data) {
                if (data.mount !== undefined) {
                    mount._add(data.mount);
                    $.bootstrapGrowl('Mount Point successfully created.', {type: 'success', align: 'center'});
                } else if (data.mounts !== undefined) {
                    // add multiple mounts
                    _.each(data.mounts, function(_mount) {
                        mount._add(_mount);
                    });
                    
                    $.bootstrapGrowl('Multiple mount points successfully created.', {type: 'success', align: 'center'});
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
    
    _update: function(mount_) {
        var tr = $('tr[data-id="' + mount_.id + '"]');
        
        _.each(mount_, function(value, key) {
            if (key === 'id') return;
            var td = tr.find('td#' + key);
            td.text(value);
        });
    },
});

