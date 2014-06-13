"use strict";

/*
 * volume
 */
var volume = {};

$.extend(volume, {
    table: null,
    
    list: function(options) {
        options = options || {};
        
        $.ajax({
            type: 'POST',
            url: '/volumes/all',
            contentType: 'application/json;charset=utf-8',
            dataType: 'json',
            data: JSON.stringify({}),
        })
        .done(function(data) {
            // console.log(data);
            _.each(data.volumes, function(volume_) {
                volume._add(volume_);
            });
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
        });
    },
    
    _add: function(volume_) {
        var tbody = volume.table.find('tbody');
        var tr_template = _.template($('#table-row-volume').html());
        var edit_template = _.template($('#modal-edit-volume').html());
        
        var tr = $(tr_template(volume_))
            .appendTo(tbody);
        
        // edit
        tr.find('a#edit').click(function(e) {
            var modal_div = $(edit_template(volume_));
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
                host_id_select.val(volume_.host_id);
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
                
                // update volume
                var _volume = {
                    id: volume_.id,
                    name: modal_div.find('#name').val(),
                    capacity: modal_div.find('#capacity').val(),
                    host_id: modal_div.find('#host_id').val(),
                    username: modal_div.find('#username').val(),
                };
                
                $.ajax({
                    type: 'POST',
                    url: '/volume/update',
                    contentType: 'application/json;charset=utf-8',
                    dataType: 'json',
                    data: JSON.stringify({
                        volume: _volume,
                    }),
                })
                .done(function(data) {
                    // required to fix variable "volume" from closure
                    _.each(_volume, function(value, key) { volume[key] = value; });
                    
                    // update UI
                    volume._update(data.volume);
                    $.bootstrapGrowl('Volume successfully updated.', {type: 'success'});
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
            // update volume
            var _volume = {
                id: volume_.id,
                active: true,
            };
            
            $.ajax({
                type: 'POST',
                url: '/volume/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    volume: _volume,
                }),
            })
            .done(function(data) {
                // required to fix variable "volume" from closure
                _.each(_volume, function(value, key) { volume[key] = value; });
                
                // update UI
                volume._update(data.volume);
                $.bootstrapGrowl('Volume activated.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        // deactivate
        tr.find('a#deactivate').click(function(e) {
            // update volume
            var _volume = {
                id: volume_.id,
                active: false,
            };
            
            $.ajax({
                type: 'POST',
                url: '/volume/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    volume: _volume,
                }),
            })
            .done(function(data) {
                // required to fix variable "volume" from closure
                _.each(_volume, function(value, key) { volume[key] = value; });
                
                // update UI
                volume._update(data.volume);
                $.bootstrapGrowl('Volume deactivated.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        // remove
        tr.find('a#remove').click(function(e) {
            $.ajax({
                type: 'POST',
                url: '/volume/remove',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    id: volume_.id,
                }),
            })
            .done(function(data) {
                tr.remove();
                $.bootstrapGrowl('User successfully removed.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
    },
    
    add: function(options) {
        options = options || {};
        var new_template = _.template($('#modal-new-volume').html());
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
            
            // create volume
            var _volume = {
                name: modal_div.find('#name').val(),
                capacity: modal_div.find('#capacity').val(),
                host_id: modal_div.find('#host_id').val(),
                username: modal_div.find('#username').val(),
            };
            
            $.ajax({
                type: 'POST',
                url: '/volume/create',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    volume: _volume,
                }),
            })
            .done(function(data) {
                volume._add(data.volume);
                $.bootstrapGrowl('Volume successfully created.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        modal_div.modal({
            backdrop: 'static',
        });
    },
    
    _update: function(volume_) {
        var tr = $('tr[data-id="' + volume_.id + '"]');
        
        _.each(volume_, function(value, key) {
            if (key === 'id') return;
            var td = tr.find('td#' + key);
            td.text(value);
        });
    },
});

