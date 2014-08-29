#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def get_url_from_ct(ct, pk):
    model = ct.model_class()
    if hasattr(model, '_erpmeta'):
        return reverse('%s:detail' % model._erpmeta.url_namespace, kwargs={'pk': pk})
    return '#'


@register.simple_tag
def get_erp_url(obj, view="detail", key=None, **kwargs):
    if hasattr(obj, '_erpmeta'):
        namespace = obj._erpmeta.url_namespace
        if view in ["detail", "update", "delete", "workflow", "report", "clone"]:
            kwargs.update({'pk': obj.pk})
        if view in ["create"] and key:
            kwargs.update({'key': key})
        return reverse('%s:%s' % (namespace, view), kwargs=kwargs)
    return '#'
