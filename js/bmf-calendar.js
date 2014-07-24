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
            base.container.append('<div class="row" style="position: relative; z-index:5; display:hidden"><div class="col-sm-6"></div><div class="col-sm-6"></div></div>');
            base.datefield = base.container.find('div.row div').first();
            base.timefield = base.container.find('div.row div').last();

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
            base.container.children('div.row').show();
            if (base.datefield.children().length == 0) {
                base.buildDateField();
            }
            if (base.timefield.children().length == 0) {
                base.buildDateField();
            }
        }

        base.destroyCalendar = function() {
            base.container.children('div.row').hide();
        }

        base.buildTimeField = function() {
            base.timefield.html('TIME');
        }

        base.buildDateField = function() {
            base.datefield.html('<table class="table-condensed"><thead><tr><th class="prev">‹</th><th colspan="5" class="switch">February 2012</th><th class="next">›</th></tr><tr><th class="dow">Su</th><th class="dow">Mo</th><th class="dow">Tu</th><th class="dow">We</th><th class="dow">Th</th><th class="dow">Fr</th><th class="dow">Sa</th></tr></thead><tbody><tr><td class="day  old">29</td><td class="day  old">30</td><td class="day  old">31</td><td class="day ">1</td><td class="day ">2</td><td class="day ">3</td><td class="day ">4</td></tr><tr><td class="day ">5</td><td class="day ">6</td><td class="day ">7</td><td class="day ">8</td><td class="day ">9</td><td class="day ">10</td><td class="day ">11</td></tr><tr><td class="day  active">12</td><td class="day ">13</td><td class="day ">14</td><td class="day ">15</td><td class="day ">16</td><td class="day ">17</td><td class="day ">18</td></tr><tr><td class="day ">19</td><td class="day ">20</td><td class="day ">21</td><td class="day ">22</td><td class="day ">23</td><td class="day ">24</td><td class="day ">25</td></tr><tr><td class="day ">26</td><td class="day ">27</td><td class="day ">28</td><td class="day ">29</td><td class="day  new">1</td><td class="day  new">2</td><td class="day  new">3</td></tr><tr><td class="day  new">4</td><td class="day  new">5</td><td class="day  new">6</td><td class="day  new">7</td><td class="day  new">8</td><td class="day  new">9</td><td class="day  new">10</td></tr></tbody></table>');
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
