"use strict";

/*
 * container
 */
var container = {};

$.extend(container, {
    table: null,
    
    list: function(options) {
        options = options || {};
        
        $.ajax({
            type: 'POST',
            url: '/containers/all',
            contentType: 'application/json;charset=utf-8',
            dataType: 'json',
            data: JSON.stringify({}),
        })
        .done(function(data) {
            // console.log(data);
            _.each(data.containers, function(container_) {
                container._add(container_);
            });
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
        });
    },
    
    add: function(options) {
        options = options || {};
        var new_template = _.template($('#modal-new-container').html());
        var modal_div = $(new_template());
        var host_id_select = modal_div.find('#host_id');
        var image_id_select = modal_div.find('#image_id');
        var volumes_select = modal_div.find('#volumes');
        
        // populate hosts
        container._populate_hosts(host_id_select);
        
        // populate images
        container._populate_images(image_id_select);
        
        // populate volumes
        container._populate_volumes(volumes_select);
        
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
            
            // create container
            var volumes = [];
            var volume = modal_div.find('#volumes').val();
            if (!!volume) volumes.push(volume);
            
            var _container = {
                name: modal_div.find('#name').val(),
                host_id: modal_div.find('#host_id').val(),
                image_id: modal_div.find('#image_id').val(),
                command: modal_div.find('#command').val(),
                volumes: volumes,
                // volumes: modal_div.find('#volumes').val(),
                // volumes_from: modal_div.find('#volumes_from').val(),
                env_vars: modal_div.find('#env_vars').val(),
                expose_ports: modal_div.find('#expose_ports').val(),
                publish_ports: modal_div.find('#publish_ports').val(),
                // link_containers: modal_div.find('#link_containers').val(),
                ram_limit: parseInt(modal_div.find('#ram_limit').val()),
                n_cpu_cores: parseInt(modal_div.find('#n_cpu_cores').val()),
                // cpu_share: modal_div.find('#cpu_share').val(),
                status: modal_div.find('#status').val(),
            };
            
            $.ajax({
                type: 'POST',
                url: '/container/create',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    container: _container,
                }),
            })
            .done(function(data) {
                container._add(data.container);
                $.bootstrapGrowl('Volume successfully created.', {type: 'success', align: 'center'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
        
        modal_div.modal({
            backdrop: 'static',
        });
    },
    
    _add: function(container_) {
        var tbody = container.table.find('tbody');
        var tr_template = _.template($('#table-row-container').html());
        
        var tr = $(tr_template(container_))
            .appendTo(tbody);
        
        // activate
        tr.find('a#activate').click(function(e) {
            // update container
            var _container = {
                id: container_.id,
                active: true,
            };
            
            $.ajax({
                type: 'POST',
                url: '/container/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    container: _container,
                }),
            })
            .done(function(data) {
                // required to fix variable "container" from closure
                _.each(_container, function(value, key) { container_[key] = value; });
                
                // update UI
                container._update(data.container);
                $.bootstrapGrowl('Volume activated.', {type: 'success', align: 'center'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
        
        // deactivate
        tr.find('a#deactivate').click(function(e) {
            // update container
            var _container = {
                id: container_.id,
                active: false,
            };
            
            $.ajax({
                type: 'POST',
                url: '/container/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    container: _container,
                }),
            })
            .done(function(data) {
                // required to fix variable "container" from closure
                _.each(_container, function(value, key) { container_[key] = value; });
                
                // update UI
                container._update(data.container);
                $.bootstrapGrowl('Volume deactivated.', {type: 'success', align: 'center'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
        
        // remove
        tr.find('a#remove').click(function(e) {
            $.ajax({
                type: 'POST',
                url: '/container/remove',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    id: container_.id,
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
    
    _update: function(container_) {
        var tr = $('tr[data-id="' + container_.id + '"]');
        
        _.each(container_, function(value, key) {
            if (key === 'id') return;
            var td = tr.find('td#' + key);
            td.text(value);
        });
    },
    
    _populate_hosts: function(host_id_select, host_id) {
        host_id_select.empty();
        
        // populate hosts
        $.ajax({
            type: 'POST',
            url: '/hosts/all',
            contentType: 'application/json;charset=utf-8',
            dataType: 'json',
            data: JSON.stringify({}),
        })
        .done(function(data) {
            // handled error
            if (data.error) {
                $.bootstrapGrowl(data.error, {type: 'info', align: 'center'});
                return;
            }
            
            var option = $('<option>')
                .attr('value', '')
                .text('')
                .appendTo(host_id_select);
            
            _.each(data.hosts, function(host_) {
                var option = $('<option>')
                    .attr('value', host_.id)
                    .text(host_.name)
                    .appendTo(host_id_select);
            });
            
            // select host
            if (!!host_id) {
                host_id_select.val(host_id);
            }
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
        });
    },
    
    _populate_images: function(image_id_select, image_id) {
        $.ajax({
            type: 'POST',
            url: '/images/all',
            contentType: 'application/json;charset=utf-8',
            dataType: 'json',
            data: JSON.stringify({}),
        })
        .done(function(data) {
            // console.log(data);
            _.each(data.images, function(image_) {
                var option = $('<option>')
                    .attr('value', image_.id)
                    .text(image_.name)
                    .appendTo(image_id_select);
            });
            
            if (!!image_id) {
                image_id_select.val(image_id);
            }
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
        });
    },
    
    _populate_volumes: function(volumes_select, volume_id) {
        $.ajax({
            type: 'POST',
            url: '/volumes/all',
            contentType: 'application/json;charset=utf-8',
            dataType: 'json',
            data: JSON.stringify({}),
        })
        .done(function(data) {
            var option = $('<option>')
                .attr('value', '')
                .text('')
                .appendTo(volumes_select);
            
            _.each(data.volumes, function(volume_) {
                var option = $('<option>')
                    .attr('value', volume_.id)
                    .text(volume_.name)
                    .appendTo(volumes_select);
            });
            
            if (!!volume_id) {
                volumes_select.val(volume_id);
            }
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
        });
    },
});

