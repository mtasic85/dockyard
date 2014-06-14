"use strict";

/*
 * account
 */
var account = {};

$.extend(account, {
    table: null,
    
    list: function(options) {
        options = options || {};
        
        $.ajax({
            type: 'POST',
            url: '/account/users/all',
            contentType: 'application/json;charset=utf-8',
            dataType: 'json',
            data: JSON.stringify({}),
        })
        .done(function(data) {
            // console.log(data);
            _.each(data.user_accounts, function(user_account) {
                account._add(user_account);
            });
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
        });
    },
    
    _add: function(user_account) {
        var tbody = account.table.find('tbody');
        var tr_template = _.template($('#table-row-user').html());
        var edit_template = _.template($('#modal-edit-user').html());
        var quota_template = _.template($('#modal-quota-user').html());
        var stat_template = _.template($('#modal-stat-user').html());
        
        var tr = $(tr_template(user_account))
            .appendTo(tbody);
        
        // edit
        tr.find('a#edit').click(function(e) {
            var modal_div = $(edit_template(user_account));
            modal_div.find('select#usertype').val(user_account.usertype);
            
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
                
                // update user account
                var _user_account = {
                    id: user_account.id,
                    username: modal_div.find('#username').val(),
                    password: modal_div.find('#password').val(),
                    email: modal_div.find('#email').val(),
                    usertype: modal_div.find('#usertype').val(),
                };
                
                $.ajax({
                    type: 'POST',
                    url: '/account/user/update',
                    contentType: 'application/json;charset=utf-8',
                    dataType: 'json',
                    data: JSON.stringify({
                        user_account: _user_account,
                    }),
                })
                .done(function(data) {
                    // required to fix variable "user_account" from closure
                    _.each(_user_account, function(value, key) { user_account_[key] = value; });
                    
                    // update UI
                    account._update(data.user_account);
                    $.bootstrapGrowl('User successfully updated.', {type: 'success'});
                })
                .error(function (xhr, ajaxOptions, thrownError) {
                    $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
                });
            });
            
            modal_div.modal({
                backdrop: 'static',
            });
        });
        
        // quota
        tr.find('a#quota').click(function(e) {
            $.ajax({
                type: 'POST',
                url: '/account/quota/get',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    username: user_account.username,
                }),
            })
            .done(function(data) {
                var user_quota = data.user_quota;
                var modal_div = $(quota_template(user_quota));
                
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
                    
                    // update user account
                    var _user_quota = {
                        id: user_quota.id,
                        username: modal_div.find('#username').val(),
                        n_images: modal_div.find('#n_images').val(),
                        n_volumes: modal_div.find('#n_volumes').val(),
                        max_volume_cap: modal_div.find('#max_volume_cap').val(),
                        max_volumes_cap: modal_div.find('#max_volumes_cap').val(),
                        n_containers: modal_div.find('#n_containers').val(),
                        max_container_cpu: modal_div.find('#max_container_cpu').val(),
                        max_containers_cpu: modal_div.find('#max_containers_cpu').val(),
                        max_container_ram: modal_div.find('#max_container_ram').val(),
                        max_containers_ram: modal_div.find('#max_containers_ram').val(),
                        n_subdomains: modal_div.find('#n_subdomains').val(),
                    };
                    
                    $.ajax({
                        type: 'POST',
                        url: '/account/quota/update',
                        contentType: 'application/json;charset=utf-8',
                        dataType: 'json',
                        data: JSON.stringify({
                            user_quota: _user_quota,
                        }),
                    })
                    .done(function(data) {
                        $.bootstrapGrowl('Quota successfully updated.', {type: 'success'});
                    })
                    .error(function (xhr, ajaxOptions, thrownError) {
                        $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
                    });
                });
                
                modal_div.modal({
                    backdrop: 'static',
                });
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        // stat
        tr.find('a#stat').click(function(e) {
            $.ajax({
                type: 'POST',
                url: '/account/stat/get',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    username: user_account.username,
                }),
            })
            .done(function(data) {
                var user_stat = data.user_stat;
                var modal_div = $(stat_template(user_stat));
                
                // close
                modal_div.find('button#close').click(function(e) {
                    // close modal
                    modal_div.modal('hide');
                    setTimeout(function() { modal_div.remove();}, 500);
                    $('.modal-backdrop').remove();
                });
                
                modal_div.modal({
                    backdrop: 'static',
                });
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        // activate
        tr.find('a#activate').click(function(e) {
            // update user account
            var _user_account = {
                id: user_account.id,
                username: user_account.username,
                active: true,
            };
            
            $.ajax({
                type: 'POST',
                url: '/account/user/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    user_account: _user_account,
                }),
            })
            .done(function(data) {
                // required to fix variable "user_account" from closure
                _.each(_user_account, function(value, key) { user_account_[key] = value; });
                
                // update UI
                account._update(data.user_account);
                $.bootstrapGrowl('User activated.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        // deactivate
        tr.find('a#deactivate').click(function(e) {
            // update user account
            var _user_account = {
                id: user_account.id,
                username: user_account.username,
                active: false,
            };
            
            $.ajax({
                type: 'POST',
                url: '/account/user/update',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    user_account: _user_account,
                }),
            })
            .done(function(data) {
                // required to fix variable "user_account" from closure
                _.each(_user_account, function(value, key) { user_account_[key] = value; });
                
                // update UI
                account._update(data.user_account);
                $.bootstrapGrowl('User deactivated.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        // remove
        tr.find('a#remove').click(function(e) {
            $.ajax({
                type: 'POST',
                url: '/account/user/remove',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    username: user_account.username,
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
    
    _update: function(user_account) {
        var tr = $('tr[data-id="' + user_account.id + '"]');
        
        _.each(user_account, function(value, key) {
            if (key === 'id') return;
            var td = tr.find('td#' + key);
            td.text(value);
        });
    },
    
    add: function(options) {
        options = options || {};
        var new_template = _.template($('#modal-new-user').html());
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
            
            // create user account
            var _user_account = {
                username: modal_div.find('#username').val(),
                password: modal_div.find('#password').val(),
                email: modal_div.find('#email').val(),
                usertype: modal_div.find('#usertype').val(),
            };
            
            $.ajax({
                type: 'POST',
                url: '/account/user/create',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    user_account: _user_account,
                }),
            })
            .done(function(data) {
                account._add(data.user_account);
                $.bootstrapGrowl('User successfully created.', {type: 'success'});
            })
            .error(function (xhr, ajaxOptions, thrownError) {
                $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
            });
        });
        
        modal_div.modal({
            backdrop: 'static',
        });
    },
});
