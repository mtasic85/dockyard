"use strict";

/*
 * template
 */
var template = {};

$.extend(template, {
    prepare_template_from_selector: function(name, selector) {
        var $el = $(selector).css('display', '');
        var el = $el[0];
        
        var html = el
            .outerHTML
            .replace(/&lt;%/g, '<%')
            .replace(/%&gt;/g, '%>');
        
        var compiled_template = _.template(html);
        
        el.remove();
        template[name] = compiled_template;
    },
    
    prepare_template: function(name, template) {
        var compiled_template = _.template(template);
        template[name] = compiled_template;
    },
});
