#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from django.template.loader import select_template
from django.template import RequestContext
from django.core.urlresolvers import resolve

from ..dashboard.forms import ViewForm
from ..viewmixins import AjaxMixin


class ModalSaveView(AjaxMixin, TemplateView):
    template_name = 'djangoerp/modal/saveview.html'

    def get_html(self, context=None):
        if hasattr(self, 'html'):
            return self.html
        template = select_template(self.get_template_names())
        self.html = template.render(RequestContext(self.request, context or self.get_context_data()))
        return self.html

    def get(self, request, *args, **kwargs):
        view = resolve(self.request.GET['pathname'])
        if self.request.GET['search']:
            search = self.request.GET['search'][1:]
        else:
            search = None

        view_name = ':'.join([view.namespace, view.url_name])

        form = ViewForm(initial={
            'url': view_name,
            'kwargs': view.kwargs,
            'search': search,
        })
        qs = form.fields['dashboard'].queryset.filter(user_id=request.user.pk, name__isnull=False)
        form.fields['dashboard'].queryset = qs

        context = self.get_context_data()
        context.update({
            'form': form,
            'full': True,
        })
        return self.render_to_json_response({'html': self.get_html(context)})

    def post(self, request, *args, **kwargs):
        form = ViewForm(self.request.POST)
        qs = form.fields['dashboard'].queryset.filter(user_id=request.user.pk, name__isnull=False)
        form.fields['dashboard'].queryset = qs

        context = self.get_context_data()
        context.update({
            'form': form,
            'full': False,
        })

        if form.is_valid():
            form.save()
            return self.render_to_json_response({'close': True})

        return self.render_to_json_response({'html': self.get_html(context), 'close': False})
