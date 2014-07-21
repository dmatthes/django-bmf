/* editform */

(function($){
    $.erp.editform = function(el, options){
        // To avoid scope issues, use 'base' instead of 'this'
        // to reference this class from internal events and functions.
        var base = this;

        // Access to jQuery and DOM versions of element
        base.$el = $(el);
        base.el = el;
      
        // Add a reverse reference to the DOM object
        base.$el.data("erp.editform", base);

        base.init = function() {
            // load options
            base.options = $.extend({}, $.erp.editform.defaultOptions, options);

            // initialization logic
            if (base.options.href == null) {
                // load target from the elements href attribute
                base.options.href = base.$el.attr('href');

            }
            base.$el.on('click', function (event) {
                event.preventDefault();
                base.open_formular();
            });
        }

        base.initialize_modal = function () {
            // initialize the modal
            $('#wrap').prepend('<div class="modal fade" id="erpmodal_edit" tabindex="-1" role="dialog" aria-hidden="true"><div class="modal-dialog modal-lg"></div></div>');
            $('#erpmodal_edit').modal({
                keyboard: true,
                show: false,
                backdrop: 'static'
            });
            // delete the modals content, if closed
            $('#erpmodal_edit').on('hidden.bs.modal', function (e) {
                $('#erpmodal_edit div.modal-dialog').empty();
            });
            // reload the page if one save has appeared
            $('#erpmodal_edit').on('hide.bs.modal', function (e) {
                if ($('#erpmodal_edit > div.page-reload').length == 1) {
                    location.reload(false);
                }
            });
        }

        base.open_formular = function () {
            // loads the formular data into the modal
            if ($('#erpmodal_edit').length == 0) { base.initialize_modal() }

            dict = $.erp.AJAX;
            dict.type = "GET";
            dict.url = base.options.href;
            $.ajax(dict).done(function( data, textStatus, jqXHR ) {
                $('#erpmodal_edit div.modal-dialog').prepend(data.html);
                $('#erpmodal_edit').modal('show');

                // TODO ..............................................................................................

            // manipulate form url
            // cause the template-tag which generates the form is not aware of the url
            var parent_object = $('#erpmodal_edit div.modal-dialog div:first-child');
            var form_object = parent_object.find('form');
            form_object.attr('action', base.options.href.split("?",1)[0]);
            // apply erp-form functions
            form_object.find('div[data-erp-inlineform=1]').erp_inlineform();
            form_object.erp_buildform();

            parent_object.find('button.erpedit-cancel').click(function (event) {
                // TODO check if there are multile forms and close modal or show next form
                $('#erpmodal_edit').modal('hide');
            });
            parent_object.find('button.erpedit-submit').click(function (event) {
            dict = $.erp.AJAX;
            dict.type = "POST";
            dict.data = form_object.serialize();
            dict.url = form_object.attr('action');
            $.ajax(dict).done(function( data, textStatus, jqXHR ) {
                    if (data.status == "valid") {
                        // TODO check if there are multile forms and close modal or show next form
                        if ($('#erpmodal_edit > div.page-reload').length == 0) {
                            $('#erpmodal_edit > div').addClass('page-reload');
                        }
                        $('#erpmodal_edit').modal('hide');
                    }
                    else {
                        html = $($.parseHTML( data.html ));
                        form_object.html(html.find('form').html())
                        form_object.find('div[data-erp-search=1]').erp_search();
                        form_object.find('div[data-erp-inlineform=1]').erp_inlineform();
                    }
                });
            });
                // TODO ..............................................................................................
            });
        }
      
        // Run initializer
        base.init();
    };

    // default options
    $.erp.editform.defaultOptions = {
        href: null,
        debug: false
    };

    // register as jquery function
    $.fn.erp_editform = function(options){
        return this.each(function(){
            (new $.erp.editform(this, options));
        });
    };
})(jQuery);
$(document).ready(function() {$('.erp-edit').erp_editform()});
