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
        base.daysOfWeekLong = gettext('Sunday Monday Tuesday Wednesday Thursday Friday Saturday').split(' ');
        base.firstDayOfWeek = parseInt(get_format('FIRST_DAY_OF_WEEK'));

        base.isLeapYear = function(year) {
            return (((year % 4)==0) && ((year % 100)!=0) || ((year % 400)==0));
        }

        base.getDaysInMonth = function(month, year) {
            var days;
            if (month==1 || month==3 || month==5 || month==7 || month==8 || month==10 || month==12) {
                days = 31;
            }
            else if (month==4 || month==6 || month==9 || month==11) {
                days = 30;
            }
            else if (month==2 && base.isLeapYear(year)) {
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
            $.bmf.buildcalendar(base.datefield);
        }

    }; // end bmf.calendar

    // default options
    $.bmf.calendar.defaultOptions = {
        href: null,
        debug: false
    };

//  // register as jquery function
//  $.fn.bmf_calendar = function(options){
//      return $(this).find('div.input-group[data-bmf-calendar]').each(function(){
//          (new $.bmf.calendar(this, options));
//      });
//  };
})(jQuery);


/* buildcalendar */


(function($){
    $.bmf.buildcalendar = function(el, options){
        // To avoid scope issues, use 'base' instead of 'this'
        // to reference this class from internal events and functions.
        var base = this;

        // Access to jQuery and DOM versions of element
        base.$el = $(el);
        base.el = el;
      
        // Add a reverse reference to the DOM object
        base.$el.data("bmf.buildcalendar", base);

        base.init = function(el) {
            // load options
            base.options = $.extend({}, $.bmf.editform.defaultOptions, options);

            // initialization logic
            var table = $('<table class="table-condensed">');

            base.draw(table);
            base.destroy();
            base.$el.append(table);
        }
      
        // set strings
        base.monthsOfYear = gettext('January February March April May June July August September October November December').split(' ');
        base.daysOfWeek = gettext('Su Mo Tu We Th Fr Sa').split(' ');
        base.daysOfWeekLong = gettext('Sunday Monday Tuesday Wednesday Thursday Friday Saturday').split(' ');
        base.firstDayOfWeek = parseInt(get_format('FIRST_DAY_OF_WEEK'));

        base.isLeapYear = function(year) {
            return (((year % 4)==0) && ((year % 100)!=0) || ((year % 400)==0));
        }

        base.getDaysInMonth = function(month, year) {
            var days;
            if (month==1 || month==3 || month==5 || month==7 || month==8 || month==10 || month==12) {
                days = 31;
            }
            else if (month==4 || month==6 || month==9 || month==11) {
                days = 30;
            }
            else if (month==2 && base.isLeapYear(year)) {
                days = 29;
            }
            else {
                days = 28;
            }
            return days;
        };

        base.destroy = function() {
            base.$el.children().remove();
        }

        base.getWeek = function(year, month, day) {
            var date = new Date(year, month-1, day - base.firstDayOfWeek);
            date.setHours(0, 0, 0, 0);
            // Thursday in current week decides the year.
            date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
            // January 4 is always in week 1.
            var week = new Date(year, 0, 4);
            // Adjust to Thursday in week 1 and count number of weeks from date to week.
            return 1 + Math.round(((date.getTime() - week.getTime()) / 86400000 - 3 + (week.getDay() + 6) % 7) / 7);
        }

        base.draw = function(el, month, year) {
            var today = new Date();
            var todayDay = today.getDate();
            var todayMonth = today.getMonth()+1;
            var todayYear = today.getFullYear();

            thead = $('<thead>');
            tbody = $('<tbody>');

            el.append(thead, tbody);

            month = parseInt(month);
            year = parseInt(year);

            if (!month) month = todayMonth;
            if (!year) year = todayYear;

            thead.append('<tr><th class="text-center">' + year + '</th><th class="text-center">&lt;</th><th colspan="5" class="text-center">' + base.monthsOfYear[month-1] + '</th><th class="text-center">&gt;</th></tr>');

            var tr = $('<tr>');
            tbody.append(tr);
            tr.append('<td>');
            for (var i = 0; i < 7; i++) {
                tr.append('<td class="text-center">'+ base.daysOfWeek[(i + base.firstDayOfWeek) % 7] +'</td>');
            }

            var startingPos = new Date(year, month-1, 1 - base.firstDayOfWeek).getDay();
            var days = base.getDaysInMonth(month, year);

            var tr = $('<tr>');
            tbody.append(tr);

            // empty days 
            for (var i = 0; i < startingPos; i++) {
                tr.append('<td class="noday"></td>');
            }

            var currentDay = 1;
            for (var i = startingPos; currentDay <= days; i++) {
                if (i%7 == 0) {
                    tr.prepend('<td class="text-center">' + base.getWeek(year, month, currentDay) + '</td>');
                }
                if (i%7 == 0 && currentDay != 1) {
                    tr = $('<tr>');
                    tbody.append(tr);
                }
                var td = $('<td class="text-center">' + currentDay +'</td>');

//              if ((currentDay==todayDay) && (month==todayMonth) && (year==todayYear)) {
//                  todayClass='today';
//              } else {
//                  todayClass='';
//              }
//
//              // use UTC function; see above for explanation.
//              if (isSelectedMonth && currentDay == selected.getUTCDate()) {
//                  if (todayClass != '') todayClass += " ";
//                  todayClass += "selected";
//              }
//
//              var cell = quickElement('td', tableRow, '', 'class', todayClass);
//
//              quickElement('a', cell, currentDay, 'href', 'javascript:void(' + callback + '('+year+','+month+','+currentDay+'));');
//
                tr.append(td);
                currentDay++;
            }
            tr.prepend('<td class="text-center">' + base.getWeek(year, month, currentDay - 1) + '</td>');
        }

        // Run initializer
        base.init();
    }; // end bmf.buildcalendar

    // default options
    $.bmf.buildcalendar.defaultOptions = {
        long_names: false,
        callback_month: null,
        callback_week: null,
        callback_day: null,
        href_year: false,
        href_month: false,
        href_week: false,
        href_day: false,
        debug: false
    };
})(jQuery);
