#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import template
from django.utils.safestring import mark_safe

import markdown

from ..utils.markdown.urlize import UrlizeExtension
from ..utils.markdown.checklist import ChecklistExtension

register = template.Library()


@register.filter(name="erpmarkup")
def markdown_filter(text):
    """
    """
    if not text:
        return ''
    return mark_safe(markdown.markdown(text, extensions=[
            UrlizeExtension(),
            ChecklistExtension(),
            'smart_strong',
            'sane_lists',
            'smarty',
        ],
        output_format="html5",
        save_mode = 'escape',
        smart_emphasis = True,
        lazy_ol = True,
    ))
markdown_filter.is_safe = True
