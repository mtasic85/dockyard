"use strict";

/*
 * domain
 */
var domain = {};

$.extend(domain, {
    table: null,
    
    list: function(options) {
        options = options || {};
        
        $.ajax({
            type: 'POST',
            url: '/network/domains/all',
            contentType: 'application/json;charset=utf-8',
            dataType: 'json',
            data: JSON.stringify({}),
        })
        .done(function(data) {
            // console.log(data);
            _.each(data.domains, function(domain_) {
                domain._add(domain_);
            });
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
        });
    },
    
    _add: function(domain_) {
        var tbody = domain.table.find('tbody');
        var tr_template = _.template($('#table-row-domain').html());
        var edit_template = _.template($('#modal-edit-domain').html());
        
        var tr = $(tr_template(domain_))
            .appendTo(tbody);
        
        // edit
        tr.find('a#edit').click(function(e) {
            var modal_div = $(edit_template(domain_));
            
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
                
                // update domain
                var _domain = {
                    id: domain_.id,
                    domain: modal_div.find('#domain').val(),
                    username: modal_div.find('#username').val(),
                };
                
                $.ajax({
                    type: 'POST',
                    url: '/network/domain/update',
                    contentType: 'application/json;charset=utf-8',
                    dataType: 'json',
                    data: JSON.stringify({
                        domain: _domain,
                    }),
                })
                .done(function(data) {
                    // required to fix variable "domain" from closure
                    _.each(_domain, function(value, key) { domain_[key] = value; });
                    
                    // update UI
                    domain._update(data.domain);
                    $.bootstrapGrowl('Host successfully updated.', {type: 'success'});
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
            // update domain
            var _domain = {
                id: domain_.id,
                active: true,
            };
            
            $.ajax({
                type: 'POST',
                url: '/network/domain/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    domain: _domain,
                }),
            })
            .done(function(data) {
                // required to fix variable "domain" from closure
                _.each(_domain, function(value, key) { domain_[key] = value; });
                
                // update UI
                domain._update(data.domain);
                $.bootstrapGrowl('Host activated.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        // deactivate
        tr.find('a#deactivate').click(function(e) {
            // update domain
            var _domain = {
                id: domain.id,
                active: false,
            };
            
            $.ajax({
                type: 'POST',
                url: '/network/domain/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    domain: _domain,
                }),
            })
            .done(function(data) {
                // required to fix variable "domain" from closure
                _.each(_domain, function(value, key) { domain_[key] = value; });
                
                // update UI
                domain._update(data.domain);
                $.bootstrapGrowl('Host deactivated.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        // remove
        tr.find('a#remove').click(function(e) {
            $.ajax({
                type: 'POST',
                url: '/network/domain/remove',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    id: domain_.id,
                }),
            })
            .done(function(data) {
                tr.remove();
                $.bootstrapGrowl('Host successfully removed.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
    },
    
    add: function(options) {
        options = options || {};
        var new_template = _.template($('#modal-new-domain').html());
        var modal_div = $(new_template());
        
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
            
            // create domain
            var _domain = {
                domain: modal_div.find('#domain').val(),
                username: modal_div.find('#username').val(),
            };
            
            $.ajax({
                type: 'POST',
                url: '/network/domain/create',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    domain: _domain,
                }),
            })
            .done(function(data) {
                domain._add(data.domain);
                $.bootstrapGrowl('Host successfully created.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        modal_div.modal({
            backdrop: 'static',
        });
    },
    
    _update: function(domain_) {
        var tr = $('tr[data-id="' + domain_.id + '"]');
        
        _.each(domain_, function(value, key) {
            if (key === 'id') return;
            var td = tr.find('td#' + key);
            td.text(value);
        });
    },
});
