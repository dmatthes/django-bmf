#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
# from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.text import force_text
from django.utils.timezone import now
from django.views.defaults import permission_denied
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .models import Activity
from .models import Notification
from .forms import HistoryCommentForm


from ..viewmixins import ViewMixin
from ..viewmixins import AjaxMixin

from ..settings import ACTIVITY_WORKFLOW
from ..settings import ACTIVITY_COMMENT
from ..settings import ACTIVITY_UPDATED
from ..settings import ACTIVITY_FILE
from ..settings import ACTIVITY_CREATED

from ..signals import activity_comment

from ..sites import site

import logging
logger = logging.getLogger(__name__)


class NotificationView(ViewMixin, ListView):
    model = Notification
    allow_empty = True
    template_name = "djangobmf/notification/index.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        selected_ct_id = int(self.kwargs.get('ct', 0))
        selected_model = None

        # Dict with all items of right navigation
        navigation = {}

        # prefill
        for ct, model in site.models.items():
            info = model._meta.app_label, model._meta.model_name
            perm = '%s.view_%s' % info

            if ct == selected_ct_id:
                selected_model = model

            if model._bmfmeta.has_activity:
                navigation[ct] = {
                    'name': force_text(model._meta.verbose_name_plural),
                    'count': 0,
                    'ct': ct,
                    'visible': self.request.user.has_perm(perm),
                }

        total = 0
        qs = Notification.objects.exclude(watch_id__isnull=True).filter(user=self.request.user, unread=True)
        # FIXME: The query used here should use SQL to distinct select and count the db
        for data in qs.annotate(count=Count('unread')).values('watch_ct', 'count'):
            navigation[data['watch_ct']]['visible'] = True
            navigation[data['watch_ct']]['count'] += data['count']
            total += data['count']

        # update notification icon if neccessary
        sessiondata = self.request.session.get('djangobmf', None)
        if sessiondata and total != sessiondata.get('notification_count', -1):
            self.update_notification(total)

        kwargs.update({
            'navigation': navigation.values(),
            'unread': total,
            'selected_ct': selected_ct_id,
            'datafilter': self.kwargs.get('filter', None),
            'symbols': {
                'workflow': ACTIVITY_WORKFLOW,
                'comment': ACTIVITY_COMMENT,
                'updated': ACTIVITY_UPDATED,
                'file': ACTIVITY_FILE,
                'created': ACTIVITY_CREATED,
            }
        })

        # load settings for specific category
        if selected_model and navigation[selected_ct_id]['visible']:
            default, created = Notification.objects.get_or_create(
                user=self.request.user,
                watch_ct_id=selected_ct_id,
                watch_id=None,
                unread=False,
            )

            if created:
                logger.debug("Notifications object (%s) created for %s" % (default.pk, self.request.user))

            kwargs.update({
                'glob_settings': default,
                'has_detectchanges': selected_model._bmfmeta.has_detectchanges,
                'has_files': selected_model._bmfmeta.has_files,
                'has_comments': selected_model._bmfmeta.has_comments,
                'has_workflow': selected_model._bmfmeta.has_workflow,
            })

        return super(NotificationView, self).get_context_data(**kwargs)

    def get_queryset(self):

        qs = Notification.objects.exclude(watch_id__isnull=True).filter(user=self.request.user)

        filter = self.kwargs.get('filter', "unread")

        if filter == "unread":
            qs = qs.filter(unread=True)

        if filter == "active":
            qs = qs.filter(triggered=True)

        if self.kwargs.get('ct', None):
            qs = qs.filter(watch_ct_id=self.kwargs.get('ct'))

        return qs.select_related('activity', 'ct', 'created_by')


class NotificationCreate(AjaxMixin, CreateView):
    model = Notification
    template_name = "djangobmf/notification/create.html"
    fields = ('new_entry', 'comment', 'file', 'changed', 'workflow')

    # FIXME CHECK OBJECT PERMISSIONS!

    def get_cls(self):
        return ContentType.objects.get_for_id(self.kwargs['ct']).model_class()

    def get_form(self, form_class):
        form = super(NotificationCreate, self).get_form(form_class)
        cls = self.get_cls()

        del form.fields['new_entry']
        if not cls._bmfmeta.has_detectchanges:
            del form.fields['changed']
        if not cls._bmfmeta.has_files:
            del form.fields['file']
        if not cls._bmfmeta.has_comments:
            del form.fields['comment']
        if not cls._bmfmeta.has_workflow:
            del form.fields['workflow']

        return form

    def form_valid(self, form):
        notification = form.save(commit=False)
        notification.user = self.request.user
        notification.watch_ct = ContentType.objects.get_for_id(self.kwargs['ct'])
        notification.watch_id = int(self.kwargs['pk'])
        notification.triggered = False
        notification.unread = False
        notification.save()
        return self.render_valid_form({'refresh': True, 'redirect': None})


class NotificationUpdate(AjaxMixin, UpdateView):
    model = Notification
    template_name = "djangobmf/notification/update.html"
    fields = ('new_entry', 'comment', 'file', 'changed', 'workflow')

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.save()
        return self.render_valid_form({'refresh': True, 'redirect': None})

    def get_object(self):
        if hasattr(self, 'object') and hasattr(self, 'rel_cls'):
            return self.object
        self.object = super(NotificationUpdate, self).get_object()
        self.rel_cls = self.object.watch_ct.model_class()
        return self.object

    def get_form(self, form_class):
        form = super(NotificationUpdate, self).get_form(form_class)
        if self.object.watch_id:
            del form.fields['new_entry']
        if not self.rel_cls._bmfmeta.has_detectchanges:
            del form.fields['changed']
        if not self.rel_cls._bmfmeta.has_files:
            del form.fields['file']
        if not self.rel_cls._bmfmeta.has_comments:
            del form.fields['comment']
        if not self.rel_cls._bmfmeta.has_workflow:
            del form.fields['workflow']
        return form


class ActivityView(ListView):
    """
    table view
    """
    model = Notification
    allow_empty = True
    template_name = "djangobmf/activity_list.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ActivityView, self).dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(ActivityView, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user).select_related('history', 'ct')


class HistoryCommentAddView(CreateView):
    """
    table view
    """
    model = Activity
    form_class = HistoryCommentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.has_perms(self.get_permissions([])):
            return permission_denied(self.request)
        return super(HistoryCommentAddView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_rel_model(self):
        if hasattr(self, 'related_model'):
            return self.related_model
        try:
            ct = ContentType.objects.get_for_id(self.kwargs['ct'])
        except ContentType.DoesNotExist:
            raise Http404

        self.related_model = ct.model_class()
        if not hasattr(self.related_model, '_bmfmeta'):
            raise Http404

        return self.related_model

    def form_valid(self, form):
        if form.instance.text or form.instance.topic:
            form.instance.user = self.request.user
            form.instance.parent_id = self.kwargs['pk']
            form.instance.parent_ct = ContentType.objects.get_for_id(self.kwargs['ct'])
            self.object = form.save()
            self.object.parent_object.modified = now()
            self.object.parent_object.modified_by = self.request.user
            self.object.parent_object.save()
            activity_comment.send(sender=self.object.__class__, instance=self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_rel_object(self):
        if hasattr(self, 'related_object'):
            return self.related_object
        try:
            self.related_object = self.get_rel_model().objects.get(pk=self.kwargs['pk'])
        except self.get_rel_model().DoesNotExist:
            raise Http404

        return self.related_object

    def get_permissions(self, perms):
        info = self.get_rel_model()._meta.app_label, self.get_rel_model()._meta.model_name
        perms.append('%s.view_%s' % info)
        return perms

    def get_success_url(self):
        return self.get_rel_object().bmfmodule_detail()
