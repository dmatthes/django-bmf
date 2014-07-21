$(document).ready(function() {

    /* Notification
     * ----------------------------------------------------------------------- */

    function check_notification() {
        var count = parseInt( $('#erp_notification').data('count') );
        if (count > 0) {
            $('#erp_notification').removeClass("new").addClass("new");
        }
    }
    check_notification();

    /* Message
     * ----------------------------------------------------------------------- */
    /*
    $('#erp_message').click(function (event) {
        event.preventDefault();
        if ($('#erpmodal_logout').length == 0) {
            $.get($(this).attr('href'), function(data) {
                $('#wrap').prepend('<div class="modal fade" id="erpmodal_logout" tabindex="-1" role="dialog" aria-hidden="true">'+data+'</div>');
                $('#erpmodal_logout').modal('show');
            });
        }
        else {
            $('#erpmodal_logout').modal('show');
        }
    });
   
    /* LOGOUT
     * ----------------------------------------------------------------------- */
    $('#erpapi_logout').click(function (event) {
        event.preventDefault();
        if ($('#erpmodal_logout').length == 0) {
            $.get($(this).attr('href'), function(data) {
                $('#wrap').prepend('<div class="modal fade" id="erpmodal_logout" tabindex="-1" role="dialog" aria-hidden="true">'+data+'</div>');
                $('#erpmodal_logout').modal('show');
            });
        }
        else {
            $('#erpmodal_logout').modal('show');
        }
    });
   
    /* SAVE VIEW
     * ----------------------------------------------------------------------- */
    $('#erpapi_saveview').click(function (event) {
        event.preventDefault();
        if ($('#erpmodal_saveview').length == 0) {
            $('#wrap').prepend('<div class="modal fade" id="erpmodal_saveview" tabindex="-1" role="dialog" aria-hidden="true"></div>');
        }
        var search = $(location).attr('search');
        var pathname = $(location).attr('pathname');
        var url = $(this).attr('href');
        dict = $.erp.AJAX;
        dict.type = 'GET';
        dict.data = { search: search, pathname: pathname };
        dict.url = url;
        $.ajax(dict)
            .done(function( data, textStatus, jqXHR ) {
                $('#erpmodal_saveview').html(data.html);
                $('#erpmodal_saveview').modal('show');
                $('#erpmodal_saveview form').submit(function(event){
                    event.preventDefault();
                    dict = $.erp.AJAX;
                    dict.type = 'POST';
                    dict.data = $(this).serialize();
                    dict.url = url;
                    $.ajax(dict)
                      .done(function( data, textStatus, jqXHR ) {
                          if (data.close == true) {
                             $('#erpmodal_saveview .modal-body').html("TODO REFRESH PAGE");
                          }
                          else {
                             $('#erpmodal_saveview .modal-body').html(data.html);
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


    $('#erpapi_follow').click(function (event) {
        event.preventDefault();
        if ($('#erpmodal_follow').length == 0) {
            var ct = $(this).data('ct');
            var pk = $(this).data('pk');
            var url = $(this).attr('href');
            dict = $.erp.AJAX;
            dict.type = 'GET';
            dict.data = { ct: ct, pk: pk };
            dict.url = url;
            $.ajax(dict)
            .done(function( data, textStatus, jqXHR ) {
                $('#wrap').prepend('<div class="modal fade" id="erpmodal_follow" tabindex="-1" role="dialog" aria-hidden="true">'+data.html+'</div>');

                $('#erpmodal_follow').modal('show');

                $('#erpmodal_follow form').submit(function(event){
                    event.preventDefault();
                    dict = $.erp.AJAX;
                    dict.type = 'POST';
                    dict.data = $(this).serializeArray();
                    dict.data.push({name: 'ct', value: ct });
                    dict.data.push({name: 'pk', value: pk });
                    dict.data = $.param(dict.data);
                    dict.url = url;
                    $.ajax(dict)
                      .done(function( data, textStatus, jqXHR ) {
                          $('#erpapi_follow').removeClass('following');
                          $('#erpapi_follow span').removeClass('glyphicon-star glyphicon-star-empty');
                          if (data.active == true) {
                            $('#erpapi_follow').addClass('following');
                            $('#erpapi_follow span').addClass('glyphicon-star');
                          }
                          else {
                            $('#erpapi_follow span').addClass('glyphicon-star-empty');
                          }
                          $('#erpmodal_follow').modal('hide');
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
          $('#erpmodal_follow').modal('show');
        }
    });
});
