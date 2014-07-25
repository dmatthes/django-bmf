#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.template.loader import select_template
from django.template import Context

from djangoerp.sites import site
from djangoerp.report.models import BaseReport
from djangoerp.utils import get_model_from_cfg

from io import BytesIO
from xhtml2pdf import pisa
from ConfigParser import RawConfigParser


class Xhtml2PdfReport(BaseReport):

    def __init__(self, options):
        self.options = RawConfigParser(allow_no_value=True)
        self.options.readfp(BytesIO(options.encode("UTF-8")))

    def get_default_options(self):
        return """
[layout]
size = A4
form = A
letter = True

[letter_page]
margin_left = 10mm
margin_bottom = 15mm
extra = true
extra_right = 10mm
extra_top = 40mm
pdf_background_pk = None

[pages]
margin_left = 10mm
margin_bottom = 15mm
margin_top = 20mm
footer_right = 10mm
footer_height = 10mm
pdf_background_pk = None
  """

    def get_output_formats(self):
        return ('pdf',)

    def render(self, request, context):
        buffer = BytesIO()
        model = context['erpmodule']['model']._meta
        template_name = '%s/%s_htmlreport.html' % (model.app_label, model.model_name)

        document = get_model_from_cfg('DOCUMENT')

        pages_file = None
        letter_file = None

        if self.options.has_option('pages', 'pdf_background_pk'):
            if self.options.getint('pages', 'pdf_background_pk'):
                bg_pk = self.options.getint('pages', 'pdf_background_pk')
                try:
                    file = document.objects.get(pk=bg_pk)
                    pages_file = ''.join(file.file.read().encode('base64').splitlines())
                except document.DoesNotExist:
                    pass

        if self.options.has_option('letter_page', 'pdf_background_pk'):
            if self.options.getint('letter_page', 'pdf_background_pk'):
                bg_pk = self.options.getint('letter_page', 'pdf_background_pk')
                try:
                    file = document.objects.get(pk=bg_pk)
                    letter_file = ''.join(file.file.read().encode('base64').splitlines())
                except document.DoesNotExist:
                    pass

        options = {
            'template_name': template_name,

            'size': self.options.get('layout', 'size'),
            'form': self.options.get('layout', 'form'),
            'letter': self.options.getboolean('layout', 'letter'),

            'template_letter': letter_file,
            'template_pages': pages_file,

            #  'margin_left': self.cfg.getboolean('letter_page', 'margin_left'),
            #  'margin_bottom': self.cfg.getboolean('letter_page', 'margin_bottom'),
            'extra': self.options.getboolean('letter_page', 'extra'),
            #  'extra_right': self.cfg.getboolean('letter_page', 'extra_right'),
            #  'extra_top': self.cfg.getboolean('letter_page', 'extra_top'),

        }
        context['options'] = options

        template = select_template([template_name, 'djangoerp/report_html_base.html'])
        html = template.render(Context(context))
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), buffer)  # pdf won't be UTF-8
        pdf = buffer.getvalue()
        buffer.close()
        return pdf


site.register_report('xhtml2pdf', Xhtml2PdfReport)
