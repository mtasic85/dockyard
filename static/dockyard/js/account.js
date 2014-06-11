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
        .error(function (xhr, ajaxOptions, thrownError) {});
    },
    
    _add: function(user_account) {
        var tbody = account.table.find('tbody');
        var tr_template = _.template($('#table-row-user').html());
        var edit_template = _.template($('#modal-edit-user').html());
        var quota_template = _.template($('#modal-quota-user').html());
        var stat_template = _.template($('#modal-stat-user').html());
        // var activate_template = _.template($('#modal-activate-user').html());
        // var deactivate_template = _.template($('#modal-deactivate-user').html());
        // var remove_template = _.template($('#modal-remove-user').html());
        
        var tr = $(tr_template(user_account))
            .appendTo(tbody);
        
        // edit
        tr.find('a#edit').click(function(e) {
            var modal_div = $(edit_template(user_account));
            
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
                });
                
                modal_div.modal({
                    backdrop: 'static',
                });
            })
            .error(function (xhr, ajaxOptions, thrownError) {});
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
            .error(function (xhr, ajaxOptions, thrownError) {});
        });
        
        // activate
        tr.find('a#activate').click(function(e) {
            $.ajax({
                type: 'POST',
                url: '/account/activate',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    username: user_account.username,
                }),
            })
            .done(function(data) {})
            .error(function (xhr, ajaxOptions, thrownError) {});
        });
        
        // deactivate
        tr.find('a#deactivate').click(function(e) {
            $.ajax({
                type: 'POST',
                url: '/account/deactivate',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    username: user_account.username,
                }),
            })
            .done(function(data) {})
            .error(function (xhr, ajaxOptions, thrownError) {});
        });
        
        // remove
        tr.find('a#remove').click(function(e) {
            $.ajax({
                type: 'POST',
                url: '/account/remove',
                contentType: 'application/json;charset=utf-8',
                dataType: 'json',
                data: JSON.stringify({
                    username: user_account.username,
                }),
            })
            .done(function(data) {})
            .error(function (xhr, ajaxOptions, thrownError) {});
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
            var user_account = {
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
                    user_account: user_account,
                }),
            })
            .done(function(data) {
                account._add(data.user_account);
            })
            .error(function (xhr, ajaxOptions, thrownError) {});
        });
        
        modal_div.modal({
            backdrop: 'static',
        });
    },
});
