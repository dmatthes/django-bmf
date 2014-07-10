$(document).ready(function() {

    /* Load form modal
     * ----------------------------------------------------------------------- */

    $('.erp-edit').click(function (event) {
        event.preventDefault();
        var form_target = $(this).attr('href');

        // initialize the modal
        if ($('#erpmodal_edit').length == 0) {
            $('#wrap').prepend('<div class="modal fade" id="erpmodal_edit" tabindex="-1" role="dialog" aria-hidden="true"><div class="modal-dialog modal-lg"></div></div>');
            $('#erpmodal_edit').modal({
                keyboard: true,
                show: false,
                backdrop: 'static'
            });
            // delete the modals content, if closed
            $('#erpmodal_edit').on('hidden.bs.modal', function (e) {
                $('#erpmodal_edit div.modal-dialog').empty();
            });
            // reload the page if one save has appeared
            $('#erpmodal_edit').on('hide.bs.modal', function (e) {
                if ($('#erpmodal_edit > div.page-reload').length == 1) {
                    location.reload(false);
                }
            });
        }
        // get the new content for the modal
        $.get(form_target, function(data) {
            $('#erpmodal_edit div.modal-dialog').prepend(data);
            $('#erpmodal_edit').modal('show');
        }).done( function() {
            // manipulate form url
            // cause the template-tag which generates the form is not aware of the url
            var parent_object = $('#erpmodal_edit div.modal-dialog div:first-child');
            var form_object = parent_object.find('form');
            form_object.attr('action', form_target);
            // apply erp-form functions
            form_object.find('div[data-erp-search=1]').djangoerp_search();
            form_object.find('div[data-erp-inlineform=1]').djangoerp_inlineform();

            parent_object.find('button.erpedit-cancel').click(function (event) {
                // TODO check if there are multile forms and close modal or show next form
                $('#erpmodal_edit').modal('hide');
            });
            parent_object.find('button.erpedit-submit').click(function (event) {
            dict = ERPAJAX;
            dict.dataType = 'html';
            dict.type = "POST";
            dict.data = form_object.serialize();
            dict.url = form_object.attr('action');
            $.ajax(dict).done(function( data, textStatus, jqXHR ) {
                    if (data == "ok") {
                        // TODO check if there are multile forms and close modal or show next form
                        if ($('#erpmodal_edit > div.page-reload').length == 0) {
                            $('#erpmodal_edit > div').addClass('page-reload');
                        }
                        $('#erpmodal_edit').modal('hide');
                    }
                    else {
                        html = $($.parseHTML( data ));
                        form_object.html(html.find('form').html())
                        form_object.find('div[data-erp-search=1]').djangoerp_search();
                        form_object.find('div[data-erp-inlineform=1]').djangoerp_inlineform();
                    }
                }).fail(function(jqXHR, textStatus, errorThrown) {
                    console.log( errorThrown+" ("+textStatus+")" );
                });
            });
        });
    });
});
