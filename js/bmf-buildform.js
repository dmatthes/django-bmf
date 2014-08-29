/* buildform */
(function($){
    // register as jquery function
    $.fn.bmf_buildform = function(){
      //$(this).bmf_inlineform();
      //$(this).bmf_search();
        $(this).bmf_autocomplete();
        $(this).bmf_calendar();
    };
})(jQuery);
