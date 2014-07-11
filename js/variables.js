var ERPAJAX = {
    crossDomain: false,
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
    },
    dataType: 'json',
    statusCode: {
        403: function() {
            alert( "no permission" );
        },
        404: function() {
            alert( "not found" );
        },
        500: function() {
            alert( "server error" );
        }
    }
};
