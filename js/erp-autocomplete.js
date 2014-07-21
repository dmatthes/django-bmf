/* calendar */

/*
<div class="form-group">
    <label class="control-label">Employee</label>
    <div>
        <div class="input-group" data-erp-autocomplete="1">
            <input class="form-control" id="erp_NAME-value" placeholder="VALUE" type="text">
        </div>
        <input autocomplete="off" id="erp_NAME" type="text">
    </div>
</div>
*/

(function($){
    $.erp.autocomplete = function(el, options){
        // To avoid scope issues, use 'base' instead of 'this'
        // to reference this class from internal events and functions.
        var base = this;

        // Access to jQuery and DOM versions of element
        base.$el = $(el);
        base.el = el;
      
        // Add a reverse reference to the DOM object
        base.$el.data("erp.autocomplete", base);

        base.init = function() {
            // load options
            base.options = $.extend({}, $.erp.autocomplete.defaultOptions, options);
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
            base.input = base.$el.children('input[type="text"]').last();
            base.hidden = base.container.children('input[type="text"]').first();
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
                if (e.keyCode == $.erp.KEYS.ESC) {
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
    $.erp.autocomplete.defaultOptions = {
        // Wait 250 ms until the last key action until the request is send
        wait: 250,
        debug: true,
        // Which filter options are submitted
        url: './form-api/',
    };

    // register as jquery function
    $.fn.erp_autocomplete = function(options){
        return $(this).find('div.input-group[data-erp-autocomplete]').each(function(){
            (new $.erp.autocomplete(this, options));
        });
    };
})(jQuery);
