/* inline form */

(function($){
    $.bmf.inlineform = function(el, options){
        // To avoid scope issues, use 'base' instead of 'this'
        // to reference this class from internal events and functions.
        var base = this;

        // Access to jQuery and DOM versions of element
        base.$el = $(el);
        base.el = el;
      
        // Add a reverse reference to the DOM object
        base.$el.data("bmf.inlineform", base);

        base.init = function() {
            base.options = $.extend({}, $.bmf.inlineform.defaultOptions, options);
            base.$el.css('position','relative');
            // Put your initialization code here
            var regex_max = /(.*)-MAX_NUM_FORMS$/;
            var regex_total = /.*-TOTAL_FORMS$/;
            base.$el.find('input').each( function (el) {
              if (regex_max.test($(this).attr('id'))) {
                base.id_prefix = regex_max.exec($(this).attr('id'))[1];
                base.name_prefix = regex_max.exec($(this).attr('name'))[1];
                base.max_num_forms = parseInt($(this).attr('value'));
              }
              if (regex_total.test($(this).attr('id'))) {
                base.total_forms = parseInt($(this).attr('value'));
              }
            });

            base.container = base.$el.find('.panel').first();
            base.add_button = base.container.find('.panel-footer button.btn-success').first();
            base.form_list = base.container.find('div.list-group-item');
            base.template = base.form_list.last().hide()

            base.add_button.on('click', function (event) {
              base.addLine();
              event.preventDefault();
            });
        }

        base.addLine = function () {
            // Clone a form (without event handlers) from the first form
            var row = base.template.clone(false).insertAfter( base.container.find('div.list-group-item').last() ).slideDown(300);
            // remove errors
            row.find('.has-error').removeClass('has-error');
            row.find('.is-error').remove();

            // Relabel/rename all the relevant bits
            $('#'+base.id_prefix + '-TOTAL_FORMS').val(base.total_forms + 1);
            var id_regex = new RegExp('(' + base.id_prefix + '-\\d+-)');
            var id_replacement = base.id_prefix + '-' + base.total_forms + '-';

            var name_regex = new RegExp('(' + base.name_prefix + '-\\d+-)');
            var name_replacement = base.name_prefix + '-' + base.total_forms + '-';

            row.find('[id^='+base.id_prefix+']').each(function(){
              this.id = this.id.replace(id_regex, id_replacement);
            });
            row.find('[name^='+base.name_prefix+']').each(function(){
              this.name = this.name.replace(name_regex, name_replacement);
            });
            base.total_forms += 1;
            row.bmf_buildform();
        };

        // Run initializer
        base.init();
    };

    // default options
    $.bmf.autocomplete.defaultOptions = {
        debug: false,
    };

    // register as jquery function
    $.fn.bmf_inlineform = function(options){
        return $(this).find('div[data-bmf-inlineform]').each(function(){
            (new $.bmf.inlineform(this, options));
        });
    };
})(jQuery);
