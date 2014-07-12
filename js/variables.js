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
            alert( gettext("Error 403\n You don't have permission to view this page") );
        },
        404: function(jqXHRm, textStatus, errorThrown) {
            alert( gettext("Error 404\n Page not found") );
        },
        500: function(jqXHRm, textStatus, errorThrown) {
            alert( gettext("Error 500\n An Error occured while rendering the page") );
        }
    }
};
