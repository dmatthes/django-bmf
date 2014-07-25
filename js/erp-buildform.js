/* buildform */
(function($){
    // register as jquery function
    $.fn.erp_buildform = function(){
      //$(this).erp_inlineform();
      //$(this).erp_search();
        $(this).erp_autocomplete();
        $(this).erp_calendar();
    };
})(jQuery);
