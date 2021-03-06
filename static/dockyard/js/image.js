"use strict";

/*
 * image
 */
var image = {};

$.extend(image, {
    table: null,
    
    list: function(options) {
        options = options || {};
        
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
                image._add(image_);
            });
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
        });
    },
    
    _add: function(image_) {
        var tbody = image.table.find('tbody');
        var tr_template = _.template($('#table-row-image').html());
        
        var tr = $(tr_template(image_))
            .appendTo(tbody);
        
        // activate
        tr.find('a#activate').click(function(e) {
            // update image
            var _image = {
                id: image_.id,
                active: true,
            };
            
            $.ajax({
                type: 'POST',
                url: '/image/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    image: _image,
                }),
            })
            .done(function(data) {
                // required to fix variable "image" from closure
                _.each(_image, function(value, key) { image_[key] = value; });
                
                // update UI
                image._update(data.image);
                $.bootstrapGrowl('Image activated.', {type: 'success', align: 'center'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
        
        // deactivate
        tr.find('a#deactivate').click(function(e) {
            // update image
            var _image = {
                id: image_.id,
                active: false,
            };
            
            $.ajax({
                type: 'POST',
                url: '/image/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    image: _image,
                }),
            })
            .done(function(data) {
                // required to fix variable "image" from closure
                _.each(_image, function(value, key) { image_[key] = value; });
                
                // update UI
                image._update(data.image);
                $.bootstrapGrowl('Image deactivated.', {type: 'success', align: 'center'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
        
        // remove
        tr.find('a#remove').click(function(e) {
            $.ajax({
                type: 'POST',
                url: '/image/remove',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    id: image_.id,
                }),
            })
            .done(function(data) {
                tr.remove();
                $.bootstrapGrowl('Image successfully removed.', {type: 'success', align: 'center'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
    },
    
    add: function(options) {
        options = options || {};
        var new_template = _.template($('#modal-new-image').html());
        var modal_div = $(new_template());
        var host_id_select = modal_div.find('#host_id');
        
        // populate hosts
        image._populate_hosts(host_id_select);
        
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
            
            // create image
            var _image = {
                name: modal_div.find('#name').val(),
                host_id: modal_div.find('#host_id').val(),
                username: modal_div.find('#username').val(),
            };
            
            $.ajax({
                type: 'POST',
                url: '/image/create',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    image: _image,
                }),
            })
            .done(function(data) {
                image._add(data.image);
                $.bootstrapGrowl('Image successfully created.', {type: 'success', align: 'center'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info', align: 'center'});
            });
        });
        
        modal_div.modal({
            backdrop: 'static',
        });
    },
    
    _update: function(image_) {
        var tr = $('tr[data-id="' + image_.id + '"]');
        
        _.each(image_, function(value, key) {
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
            
            // console.log(data);
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
});

