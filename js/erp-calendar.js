/* calendar */

(function($){
    $.erp.calendar = function(el, options){
        // To avoid scope issues, use 'base' instead of 'this'
        // to reference this class from internal events and functions.
        var base = this;

        // Access to jQuery and DOM versions of element
        base.$el = $(el);
        base.el = el;
      
        // Add a reverse reference to the DOM object
        base.$el.data("erp.calendar", base);

        base.init = function() {
            // load options
            base.options = $.extend({}, $.erp.editform.defaultOptions, options);

            base.$el.append('<span class="input-group-btn"><button class="btn btn-default disabled" tabindex="-1" type="button"><span class="glyphicon glyphicon-calendar"></span></button></span>');

            // initialization logic
        }
      
        // Run initializer
        base.init();
    };

    // default options
    $.erp.calendar.defaultOptions = {
        href: null,
        debug: false
    };

    // register as jquery function
    $.fn.erp_calendar = function(options){
        return $(this).find('div.input-group[data-erp-calendar]').each(function(){
            (new $.erp.calendar(this, options));
        });
    };
})(jQuery);
