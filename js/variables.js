var ERPAJAX = {
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
    },
    crossDomain: false,
    dataType: 'json',
    error: function(jqXHRm, textStatus, errorThrown) {
        console.log( errorThrown+" ("+textStatus+")" );
        console.log(django);
    },
    statusCode: {
        403: function(jqXHRm, textStatus, errorThrown) {
            alert( gettext("no permission") );
        },
        404: function(jqXHRm, textStatus, errorThrown) {
            alert( gettext("not found") );
        },
        500: function(jqXHRm, textStatus, errorThrown) {
            alert( gettext("server error") );
        }
    }
};
