#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse


MIME_TYPES = {
    'pdf': 'application/pdf',
    'html': 'text/html',
}


class BaseReport(object):

    def __init__(self, options):
        self.options = options

    def get_default_options(self):
        raise NotImplementedError('You need to implement a get_default_options function')

    def get_output_formats(self):
        raise NotImplementedError('You need to implement a get_output_formats function')

    def render(self, request, context):
        raise NotImplementedError('You need to implement a render function')


class Report(models.Model):
    """
    Model to store informations to generate a report
    """
    reporttype = models.CharField(_("Reporttype"), max_length=20, blank=False, null=False)  # TODO replace with report field
    mimetype = models.CharField(_("Mimetype"), max_length=20, blank=False, null=False, editable=False, default="pdf")  # TODO 
    contenttype = models.ForeignKey(ContentType, related_name="erp_report", null=True, blank=True, help_text="Connect a Report to an ERP-Model", on_delete=models.CASCADE)
    options = models.TextField(_("Options"), blank=True, null=False, help_text=_("Options for the renderer. Empty this field to get all available options with default values"))  # TODO needs validator
    modified = models.DateTimeField(_("Modified"), auto_now=True, editable=False,)

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        get_latest_by = "modified"

    def __str__(self):
        return '%s' % self.contenttype

    def clean(self):
        if self.options == "":
            generator = self.get_generator()
            self.options = generator.get_default_options().strip()

    def get_generator(self):
        from djangoerp.sites import site
        return site.reports[self.reporttype](self.options)

    # response with generated file
    def render(self, request, context):
        generator = self.get_generator()

        # TODO depends on the instance of this model
        mimetype = "application/pdf"
        # FIXME: make filename from context, if context contains a object ... otherwise use report.{ext}
        filename = "report.pdf"

        file = generator.render(request, context)

        response = HttpResponse(content_type=mimetype) # TODO depends on multiple options
        if filename:
            response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        response.write(file)
        return response
