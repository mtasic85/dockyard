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
            url: '/host/all',
            contentType: 'application/json;charset=utf-8',
            dataType: 'json',
            data: JSON.stringify({}),
        })
        .done(function(data) {
            console.log(data);
            var tbody = host.table.find('tbody');
            
            _.each(data.hosts, function(host) {
                var tr = $('<tr>')
                    .appendTo(tbody);
                
                var td;
                
                // id
                td = $('<td>')
                    .text(host.id)
                    .appendTo(tr);
                
                // active
                td = $('<td>')
                    .text(host.active)
                    .appendTo(tr);
                
                // created
                td = $('<td>')
                    .text(host.created)
                    .appendTo(tr);
                
                // updated
                td = $('<td>')
                    .text(host.updated)
                    .appendTo(tr);
                
                // name
                td = $('<td>')
                    .text(host.name)
                    .appendTo(tr);
                
                // host
                td = $('<td>')
                    .text(host.host)
                    .appendTo(tr);
                
                // port
                td = $('<td>')
                    .text(host.port)
                    .appendTo(tr);
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
