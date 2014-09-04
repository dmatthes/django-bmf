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


class NotificationView(ViewMixin, ListView):
    model = Notification
    allow_empty = True
    template_name = "djangobmf/notification/index.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        navigation = super(NotificationView, self).get_queryset() \
            .values('watch_ct').annotate(count=Count('unread')).order_by()

      # total = 0
      # for data in navigation:
      #     data['name'] = force_text(
      #         ContentType.objects.get_for_id(data['obj_ct']).model_class()._meta.verbose_name_plural
      #     )
      #     total += data['count']

      # kwargs.update({
      #     'navigation': navigation,
      #     'unread': total,
      #     'selected_ct': int(self.kwargs.get('ct', 0)),
      #     'all_data': self.kwargs.get('filter', None),
      # })

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
