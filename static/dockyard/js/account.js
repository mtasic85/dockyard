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
            console.log(data);
            var tbody = account.table.find('tbody');
            var tr_template = _.template($('#table-row-user').html());
            var modal_template = _.template($('#modal-edit-user').html());
            
            _.each(data.user_accounts, function(user_account) {
                var tr = $(tr_template(user_account))
                    .appendTo(tbody);
                
                // update
                tr.find('a#edit').click(function(e) {
                    var modal_div = $(modal_template(user_account));
                    
                    modal_div.find('button#close').click(function(e) {
                        // close modal
                        modal_div.modal('hide');
                        setTimeout(function() { modal_div.remove();}, 500);
                        $('.modal-backdrop').remove();
                    });
                    
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
            });
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            
        });
    },
    
    add: function(options) {
        options = options || {};
    },
    
    update: function(options) {
        options = options || {};
    },
    
    remove: function(options) {
        options = options || {};
    },
});
