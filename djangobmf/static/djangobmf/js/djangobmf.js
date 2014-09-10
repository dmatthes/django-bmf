/*! django BMF */

(function($){
    if(!$.bmf){
        $.bmf = new Object();
    };

    // Keys
    $.bmf.KEYS = {
        ESC: 27,
        TAB: 9,
        RETURN: 13,
        UP: 38,
        DOWN: 40
    };

    $.bmf.AJAX = {
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        crossDomain: false,
        dataType: 'json',
        error: function(jqXHRm, textStatus, errorThrown) {
            console.log( errorThrown+" ("+textStatus+")" );
        },
        statusCode: {
            403: function(jqXHRm, textStatus, errorThrown) {
                alert( gettext("Error 403\n You don't have permission to view this page") );
            },
            404: function(jqXHRm, textStatus, errorThrown) {
                alert( gettext("Error 404\n Page not found") );
            },
            500: function(jqXHRm, textStatus, errorThrown) {
                alert( gettext("Error 500\n An Error occured while rendering the page") );
            }
        }
    };
})(jQuery);

$.extend($.fn.treegrid.defaults, {
    expanderExpandedClass: 'glyphicon glyphicon-minus',
    expanderCollapsedClass: 'glyphicon glyphicon-plus'
});
/* calendar */

/*
<div class="form-group">
    <label class="control-label">Employee</label>
    <div>
        <div class="input-group" data-bmf-autocomplete="1">
            <input class="form-control" id="bmf_NAME-value" placeholder="VALUE" type="text">
        </div>
        <input autocomplete="off" id="bmf_NAME" type="text">
    </div>
</div>
*/

(function($){
    $.bmf.autocomplete = function(el, options){
        // To avoid scope issues, use 'base' instead of 'this'
        // to reference this class from internal events and functions.
        var base = this;

        // Access to jQuery and DOM versions of element
        base.$el = $(el);
        base.el = el;
      
        // Add a reverse reference to the DOM object
        base.$el.data("bmf.autocomplete", base);

        base.init = function() {
            // load options
            base.options = $.extend({}, $.bmf.autocomplete.defaultOptions, options);
            if (base.options.debug) {console.log("init autocomplete")};

            // initialization logic
            base.$el.append('<span class="input-group-btn"></span>');
            base.btn = base.$el.find('.input-group-btn').first();
            base.container = base.$el.parent();

            base.btn.append('<button class="btn btn-default" tabindex="-1" type="button"><span class="glyphicon glyphicon-remove"></span></button>');
            // base.btn.append('<button class="btn btn-default" tabindex="-1" type="button"><span class="glyphicon glyphicon-plus"></span></button>');

            // base.$el.parent().css('position', 'relative');
            base.container.append('<ul class="dropdown-menu" style="display: none"></ul>');

            base.form = base.$el.parents('form').first();
            base.input = base.$el.children('input[type="text"]').first();
            base.hidden = base.container.children('input[type="hidden"]').first();
            base.dropdown = base.container.children('ul').first();
            base.input.attr('value', base.input.attr('placeholder'));
            base.timeout = false;

            // initialization logic
            // TODO ===============================================================================
            base.input.on('focus', function () {
                base.input.attr('value', '');
                base.getList();
            });
            base.input.on('blur', function () {
                window.setTimeout(function() { base.destroyList(); }, 100);
            });
            base.btn.children().on('click', function () {
                base.input.attr('value', '');
                base.input.attr('placeholder', '');
                base.hidden.attr('value', '');
            });
            base.$el.on('keyup',function () {
                base.getList();
            });
   
            $(document).keydown(function(e){
                if (e.keyCode == $.bmf.KEYS.ESC) {
                    base.destroyList();
                }
            });
        }

        // TODO ===================================================================================


    base.makeList = function(data) {
      base.dropdown.html('');
      $.each( data, function( index, obj ) {
        base.dropdown.append('<li><a href="#'+obj.pk+'">'+obj.value+'</a></li>');
      });
      base.dropdown.find('a').on('click', function (event) {
    		clicked = $(this).attr('href').match('[^#/]+$');
        base.hidden.val(clicked);
        base.input.val( $(this).html());
        base.input.attr('placeholder', $(this).html());
        base.destroyList();
        event.preventDefault();
      });
      base.dropdown.css("display","block");
    };
    
    base.destroyList = function () {
      base.input.attr('value', base.input.attr('placeholder'));
      base.dropdown.css("display","none");
    };

    base.changed = function() {
      var data = {};
      data.field = base.hidden.attr('id')
      data.form = base.form.serialize();
      //console.log(data.form);

      $.ajax({
        url: base.form.attr('action')+"form-api/?changed",
        dataType: 'json',
        type: 'post',
        data: data,
        crossDomain: false,
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
      }).done(function( data, textStatus, jqXHR ) {
        $.each( data, function( index, obj ) {
          $('#'+obj.field).attr('value', obj.value);
          $('#'+obj.field).attr('placeholder', obj.value);
        });
      }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log( errorThrown+" ("+textStatus+")" );
      });
    }
    
    base.getList = function() {
        if (base.timeout != false) {
            clearTimeout(base.timeout);
        }
        base.timeout = setTimeout(base.doGetList, base.options.wait);
    }

    base.doGetList = function () {
      base.timeout = false;
      var data = {};
      data.field = base.hidden.attr('id')
      data.form = base.form.serialize();

      data.string = base.input.val();
      if (base.hidden.val() != '') {
        data.selected = base.hidden.val()
      };

      $.ajax({
        url: base.form.attr('action')+"form-api/?search",
        dataType: 'json',
        type: 'post',
        data: data,
        crossDomain: false,
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
      }).done(function( data, textStatus, jqXHR ) {
        base.makeList(data);
      }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log( errorThrown+" ("+textStatus+")" );
      });
    };


        // TODO =======================================================================================================
      
        // Run initializer
        base.init();
    };

    // default options
    $.bmf.autocomplete.defaultOptions = {
        // Wait 250 ms until the last key action until the request is send
        wait: 250,
        debug: true,
        // Which filter options are submitted
        url: './form-api/',
    };

    // register as jquery function
    $.fn.bmf_autocomplete = function(options){
        return $(this).find('div.input-group[data-bmf-autocomplete]').each(function(){
            (new $.bmf.autocomplete(this, options));
        });
    };
})(jQuery);
/* calendar */

(function($){
    $.bmf.calendar = function(el, options){
        // To avoid scope issues, use 'base' instead of 'this'
        // to reference this class from internal events and functions.
        var base = this;

        // Access to jQuery and DOM versions of element
        base.$el = $(el);
        base.el = el;
      
        // Add a reverse reference to the DOM object
        base.$el.data("bmf.calendar", base);

        base.init = function() {
            // load options
            base.options = $.extend({}, $.bmf.editform.defaultOptions, options);

            base.$el.append('<span class="input-group-btn"><button class="btn btn-default disabled" tabindex="-1" type="button"><span class="glyphicon glyphicon-calendar"></span></button></span>');

            // initialization logic
        }
      
        // Run initializer
        base.init();
    };

    // default options
    $.bmf.calendar.defaultOptions = {
        href: null,
        debug: false
    };

    // register as jquery function
    $.fn.bmf_calendar = function(options){
        return $(this).find('div.input-group[data-bmf-calendar]').each(function(){
            (new $.bmf.calendar(this, options));
        });
    };
})(jQuery);
/* editform */

(function($){
    $.bmf.editform = function(el, options){
        // To avoid scope issues, use 'base' instead of 'this'
        // to reference this class from internal events and functions.
        var base = this;

        // Access to jQuery and DOM versions of element
        base.$el = $(el);
        base.el = el;
      
        // Add a reverse reference to the DOM object
        base.$el.data("bmf.editform", base);

        base.init = function() {
            // load options
            base.options = $.extend({}, $.bmf.editform.defaultOptions, options);

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
            $('#wrap').prepend('<div class="modal fade" id="bmfmodal_edit" tabindex="-1" role="dialog" aria-hidden="true"><div class="modal-dialog modal-lg"></div></div>');
            $('#bmfmodal_edit').modal({
                keyboard: true,
                show: false,
                backdrop: 'static'
            });
            // delete the modals content, if closed
            $('#bmfmodal_edit').on('hidden.bs.modal', function (e) {
                $('#bmfmodal_edit div.modal-dialog').empty();
            });
            // reload the page if one save has appeared
            $('#bmfmodal_edit').on('hide.bs.modal', function (e) {
                if ($('#bmfmodal_edit > div.page-reload').length == 1) {
                    location.reload(false);
                }
            });
        }

        base.open_formular = function () {
            // loads the formular data into the modal
            if ($('#bmfmodal_edit').length == 0) { base.initialize_modal() }

            dict = $.bmf.AJAX;
            dict.type = "GET";
            dict.url = base.options.href;
            $.ajax(dict).done(function( data, textStatus, jqXHR ) {
                $('#bmfmodal_edit div.modal-dialog').prepend(data.html);
                $('#bmfmodal_edit').modal('show');

                // TODO ..............................................................................................

            // manipulate form url
            // cause the template-tag which generates the form is not aware of the url
            var parent_object = $('#bmfmodal_edit div.modal-dialog div:first-child');
            var form_object = parent_object.find('form');
            form_object.attr('action', base.options.href.split("?",1)[0]);
            // apply bmf-form functions
            form_object.bmf_buildform();

            parent_object.find('button.bmfedit-cancel').click(function (event) {
                // TODO check if there are multile forms and close modal or show next form
                $('#bmfmodal_edit').modal('hide');
            });
            parent_object.find('button.bmfedit-submit').click(function (event) {
            dict = $.bmf.AJAX;
            dict.type = "POST";
            dict.data = form_object.serialize();
            dict.url = form_object.attr('action');
            $.ajax(dict).done(function( data, textStatus, jqXHR ) {
                    if (data.status == "valid") {
                        // TODO check if there are multile forms and close modal or show next form
                        if ($('#bmfmodal_edit > div.page-reload').length == 0) {
                            $('#bmfmodal_edit > div').addClass('page-reload');
                        }
                        $('#bmfmodal_edit').modal('hide');
                    }
                    else {
                        html = $($.parseHTML( data.html ));
                        form_object.html(html.find('form').html())
                        form_object.bmf_buildform();
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
    $.bmf.editform.defaultOptions = {
        href: null,
        debug: false
    };

    // register as jquery function
    $.fn.bmf_editform = function(options){
        return this.each(function(){
            (new $.bmf.editform(this, options));
        });
    };
})(jQuery);
$(document).ready(function() {
    $('.bmf-edit').bmf_editform(); // TODO: remove me
    $('.bmfedit').bmf_editform();
});
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
/* buildform */
(function($){
    // register as jquery function
    $.fn.bmf_buildform = function(){
        $(this).bmf_inlineform();
        $(this).bmf_autocomplete();
        $(this).bmf_calendar();
    };
})(jQuery);
$(document).ready(function() {

    /* Notification
     * ----------------------------------------------------------------------- */

    function check_notification() {
        var count = parseInt( $('#bmf_notification').data('count') );
        if (count > 0) {
            $('#bmf_notification').removeClass("new").addClass("new");
        }
    }
    check_notification();

    /* Message
     * ----------------------------------------------------------------------- */
    /*
    $('#bmf_message').click(function (event) {
        event.preventDefault();
        if ($('#bmfmodal_logout').length == 0) {
            $.get($(this).attr('href'), function(data) {
                $('#wrap').prepend('<div class="modal fade" id="bmfmodal_logout" tabindex="-1" role="dialog" aria-hidden="true">'+data+'</div>');
                $('#bmfmodal_logout').modal('show');
            });
        }
        else {
            $('#bmfmodal_logout').modal('show');
        }
    });
   
    /* LOGOUT
     * ----------------------------------------------------------------------- */
    $('#bmfapi_logout').click(function (event) {
        event.preventDefault();
        if ($('#bmfmodal_logout').length == 0) {
            $.get($(this).attr('href'), function(data) {
                $('#wrap').prepend('<div class="modal fade" id="bmfmodal_logout" tabindex="-1" role="dialog" aria-hidden="true">'+data.html+'</div>');
                $('#bmfmodal_logout').modal('show');
            });
        }
        else {
            $('#bmfmodal_logout').modal('show');
        }
    });
   
    /* SAVE VIEW
     * ----------------------------------------------------------------------- */
    $('#bmfapi_saveview').click(function (event) {
        event.preventDefault();
        if ($('#bmfmodal_saveview').length == 0) {
            $('#wrap').prepend('<div class="modal fade" id="bmfmodal_saveview" tabindex="-1" role="dialog" aria-hidden="true"></div>');
        }
        var search = $(location).attr('search');
        var pathname = $(location).attr('pathname');
        var url = $(this).attr('href');
        dict = $.bmf.AJAX;
        dict.type = 'GET';
        dict.data = { search: search, pathname: pathname };
        dict.url = url;
        $.ajax(dict)
            .done(function( data, textStatus, jqXHR ) {
                $('#bmfmodal_saveview').html(data.html);
                $('#bmfmodal_saveview').modal('show');
                $('#bmfmodal_saveview form').submit(function(event){
                    event.preventDefault();
                    dict = $.bmf.AJAX;
                    dict.type = 'POST';
                    dict.data = $(this).serialize();
                    dict.url = url;
                    $.ajax(dict)
                      .done(function( data, textStatus, jqXHR ) {
                          if (data.close == true) {
                             $('#bmfmodal_saveview .modal-body').html("TODO REFRESH PAGE");
                          }
                          else {
                             $('#bmfmodal_saveview .modal-body').html(data.html);
                          }
                      })
                      .fail(function(jqXHR, textStatus, errorThrown) {
                          console.log( errorThrown+" ("+textStatus+")" );
                      });
                });
            })
            .fail(function(jqXHR, textStatus, errorThrown) {
                console.log( errorThrown+" ("+textStatus+")" );
            });
    });


    $('#bmfapi_follow').click(function (event) {
        event.preventDefault();
        if ($('#bmfmodal_follow').length == 0) {
            var ct = $(this).data('ct');
            var pk = $(this).data('pk');
            var url = $(this).attr('href');
            dict = $.bmf.AJAX;
            dict.type = 'GET';
            dict.data = { ct: ct, pk: pk };
            dict.url = url;
            $.ajax(dict)
            .done(function( data, textStatus, jqXHR ) {
                $('#wrap').prepend('<div class="modal fade" id="bmfmodal_follow" tabindex="-1" role="dialog" aria-hidden="true">'+data.html+'</div>');

                $('#bmfmodal_follow').modal('show');

                $('#bmfmodal_follow form').submit(function(event){
                    event.preventDefault();
                    dict = $.bmf.AJAX;
                    dict.type = 'POST';
                    dict.data = $(this).serializeArray();
                    dict.data.push({name: 'ct', value: ct });
                    dict.data.push({name: 'pk', value: pk });
                    dict.data = $.param(dict.data);
                    dict.url = url;
                    $.ajax(dict)
                      .done(function( data, textStatus, jqXHR ) {
                          $('#bmfapi_follow').removeClass('following');
                          $('#bmfapi_follow span').removeClass('glyphicon-star glyphicon-star-empty');
                          if (data.active == true) {
                            $('#bmfapi_follow').addClass('following');
                            $('#bmfapi_follow span').addClass('glyphicon-star');
                          }
                          else {
                            $('#bmfapi_follow span').addClass('glyphicon-star-empty');
                          }
                          $('#bmfmodal_follow').modal('hide');
                      })
                      .fail(function(jqXHR, textStatus, errorThrown) {
                          console.log( errorThrown+" ("+textStatus+")" );
                      });
                });
            })
            .fail(function(jqXHR, textStatus, errorThrown) {
                console.log( errorThrown+" ("+textStatus+")" );
            });
        }
        else {
          $('#bmfmodal_follow').modal('show');
        }
    });
});
