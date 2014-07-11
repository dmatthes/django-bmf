var ERPAJAX = {
    crossDomain: false,
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
    },
    dataType: 'json',
    statusCode: {
        403: function() {
            alert( gettext("no permission") );
        },
        404: function() {
            alert( gettext("not found") );
        },
        500: function() {
            alert( gettext("server error") );
        }
    }
};
