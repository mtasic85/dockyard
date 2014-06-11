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
            _.each(data.hosts, function(host) {
                host._add(host);
            });
        })
        .error(function (xhr, ajaxOptions, thrownError) {
            $.bootstrapGrowl('Oops, something went wrong!', {type: 'info'});
        });
    },
    
    _add: function(host) {
        
    },
    
    add: function(options) {
        options = options || {};
    },
});
