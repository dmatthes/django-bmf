#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.views.generic import ListView
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.utils.text import force_text

from .models import Notification

from ..viewmixins import ViewMixin
from ..viewmixins import AjaxMixin

from ..sites import site


class NotificationView(ViewMixin, ListView):
    model = Notification
    allow_empty = True
    template_name = "djangobmf/notification/index.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):

        # Dict with all items of right navigation
        navigation = {}

        # prefill
        for ct, model in site.models.items():
            info = model._meta.app_label, model._meta.model_name
            perm = '%s.view_%s' % info

            if model._bmfmeta.has_activity:
                navigation[ct] = {
                    'name': force_text(model._meta.verbose_name_plural),
                    'count': 0,
                    'ct': ct,
                    'visible': self.request.user.has_perm(perm),
                }

        total = 0
        for data in super(NotificationView, self).get_queryset() \
                    .values('watch_ct').annotate(count=Count('unread')):
            navigation[data['watch_ct']]['visible'] = True
            navigation[data['watch_ct']]['count'] =  data['count']
            total += data['count']

        kwargs.update({
            'navigation': navigation.values(),
            'unread': total,
            'selected_ct': int(self.kwargs.get('ct', 0)),
            'datafilter': self.kwargs.get('filter', None),
        })

        return super(NotificationView, self).get_context_data(**kwargs)

    def get_queryset(self):
        qs = super(NotificationView, self).get_queryset()

        qs.exclude(watch_id__isnull=True)

        filter = self.kwargs.get('filter', "unread")

        if filter == "unread":
            qs = qs.filter(unread=True)

        if filter == "active":
            qs = qs.filter(triggered=True)

        if self.kwargs.get('ct', None):
            qs = qs.filter(watch_ct_id=self.kwargs.get('ct'))

        return qs.filter(user=self.request.user).select_related('activity', 'ct', 'created_by')
