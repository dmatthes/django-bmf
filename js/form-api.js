/*! django ERP custom js */
(function($){
  var VERSION = "0.1.0";

  if(!$.djangoerp){
      $.djangoerp = new Object();
  };

  // Keys
  var keys = {
    ESC: 27,
    TAB: 9,
    RETURN: 13,
    UP: 38,
    DOWN: 40
  };

  /*
   * 
   * SEARCH
   *
   */
          
  $.djangoerp.search = function(el, options) {
    // To avoid scope issues, use 'base' instead of 'this'
    // to reference this class from internal events and functions.
    var base = this;
    
    // Access to jQuery and DOM versions of element
    base.$el = $(el);
    base.el = el;
    
    // Add a reverse reference to the DOM object
    base.$el.data("djangoerp.search", base);

    base.init = function(){
      base.options = $.extend({}, $.djangoerp.search.defaultOptions, options);

//    base.input = base.$el.children('input[type="text"]').first();
//    base.hidden = base.$el.find('input[type="hidden"]').first();
      base.form = base.$el.parents('form').first();
      // console.log(base.form);
      base.input = base.$el.find('input[type="text"]').last();
      base.hidden = base.$el.find('input[type="text"]').first();
      base.dropdown = base.$el.children('ul').first();

      base.input.attr('value', base.input.attr('placeholder'));

      base.input.on('focus', function () {
        base.input.attr('value', '');
        base.getList();
      });
//    base.input.on('change', function () {
//      base.changed();
//    });
      base.input.on('blur', function () {
        window.setTimeout(function() { base.destroyList(); },100);
      });
      base.$el.on('keyup',function () {
        base.getList();
      });
   
     $(document).keydown(function(e){
       if (e.keyCode == keys.ESC) {
         base.destroyList();
       }
     });

    };
    
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
        base.changed();
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
      console.log(data.form);

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
    
    base.getList = function () {
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
    
    // Run initializer
    base.init();
  };
  
  $.djangoerp.search.defaultOptions = {
    // Wait 350 ms until the last key action until the request is send
    wait: 350, // TODO Not implemented
    // Which filter options are submitted
    url: './form-api/',
  };

  /*
   * 
   * MULTIFORM FUNCTIONS
   *
   */

  $.djangoerp.inlineform = function(el, options){
    // To avoid scope issues, use 'base' instead of 'this'
    // to reference this class from internal events and functions.
    var base = this;
    
    // Access to jQuery and DOM versions of element
    base.$el = $(el);
    base.el = el;
    
    // Add a reverse reference to the DOM object
    base.$el.data("djangoerp.inlineform", base);

    base.init = function() {
      base.options = $.extend({}, $.djangoerp.inlineform.defaultOptions, options);
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
    };

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
      row.find('div[data-erp-search=1]').djangoerp_search();

      // Code adapted from http://djangosnippets.org/snippets/1389/
//    function updateElementIndex(el, prefix, ndx) {
//       var id_regex = new RegExp('(' + prefix + '-\\d+-)');
//       var replacement = prefix + '-' + ndx + '-';
//       if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,replacement));
//       if (el.id) el.id = el.id.replace(id_regex, replacement);
//       if (el.name) el.name = el.name.replace(id_regex, replacement);
//    }

      console.log(base.prefix+' '+base.max_num_forms+' '+base.total_forms);
    };
    
    // Run initializer
    base.init();
  };

  $.djangoerp.inlineform.defaultOptions = {
  };

  /*
   * 
   * REGISTER FUNCTIONS TO JQUERY
   *
   */
  
   $.fn.djangoerp_search = function(options){
     return this.each(function(){
       (new $.djangoerp.search(this, options));
     });
   };
   $.fn.djangoerp_inlineform = function(options){
     return this.each(function(){
       (new $.djangoerp.inlineform(this, options));
     });
   };
})(jQuery);

//$(document).ready(function() {
//  $('div[data-erp-search=1]').djangoerp_search();
//  $("div[data-erp-inlineform=1]").djangoerp_inlineform();
//});
