$(document).ready(function() {

    ajax_dict = {
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        dataType: 'json',
        statusCode: {
            302: function() {
                alert( "REDIRECT" );
            }
            403: function() {
                alert( "no permission" );
            },
            404: function() {
                alert( "not found" );
            }
        }
    };

    /* Load form modal
     * ----------------------------------------------------------------------- */

    $('.erp-edit').click(function (event) {
        event.preventDefault();
        // initialize the modal
        if ($('#erpmodal_edit').length == 0) {
            $('#wrap').prepend('<div class="modal fade" id="erpmodal_edit" tabindex="-1" role="dialog" aria-hidden="true"><div class="modal-dialog modal-lg"></div></div>');
            $('#erpmodal_edit').modal({
                keyboard: false,
                show: false,
                backdrop: 'static'
            });
            // delete the modals content, if closed
            $('#erpmodal_edit').on('hidden.bs.modal', function (e) {
                $('#erpmodal_edit div.modal-dialog').empty();
            })
            // reload the page if one save has appeared
            $('#erpmodal_edit').on('hide.bs.modal', function (e) {
                if ($('#erpmodal_edit div.page-reload').length == 1) {
                    location.reload(false);
                }
            })
        }
        // get the new content for the modal
        $.get($(this).attr('href'), function(data) {
            $('#erpmodal_edit div.modal-dialog').prepend(data);
            $('#erpmodal_edit').modal('show');
        });
    });
});
