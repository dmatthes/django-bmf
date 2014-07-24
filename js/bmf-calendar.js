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

            base.container = base.$el.parent();

            base.$el.append('<span class="input-group-btn"><button class="btn btn-default" tabindex="-1" type="button"><span class="glyphicon glyphicon-calendar"></span></button></span>');

            base.input = base.$el.children('input[type="text"]').first();

            base.$el.find('button').first().on('click', function () {
                base.initCalendar();
            });
            base.input.on('focus', function () {
                base.initCalendar();
            });
            base.input.on('blur', function () {
                window.setTimeout(function() { base.destroyCalendar(); }, 100);
            });

            // initialization logic
        }
      
        // Run initializer
        base.init();

        // set strings
        base.monthsOfYear = gettext('January February March April May June July August September October November December').split(' ');
        base.daysOfWeek = gettext('Su Mo Tu We Th Fr Sa').split(' ');
        base.firstDayOfWeek = parseInt(get_format('FIRST_DAY_OF_WEEK'));

        base.isLeapYear = function(year) {
            return (((year % 4)==0) && ((year % 100)!=0) || ((year % 400)==0));
        }

        base.getDaysInMonth = function(month,year) {
            var days;
            if (month==1 || month==3 || month==5 || month==7 || month==8 || month==10 || month==12) {
                days = 31;
            }
            else if (month==4 || month==6 || month==9 || month==11) {
                days = 30;
            }
            else if (month==2 && CalendarNamespace.isLeapYear(year)) {
                days = 29;
            }
            else {
                days = 28;
            }
            return days;
        };
        base.initCalendar = function() {
            alert('BLUB');
        }
        base.destroyCalendar = function() {
        }

    }; // end erp.calendar

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
