#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import NoReverseMatch
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.defaults import permission_denied

from djangoerp import get_version
from djangoerp.decorators import login_required
from djangoerp.models import Notification
from djangoerp.utils import get_model_from_cfg

import json
import datetime
import urlparse

# TO BE USED IN EVERY ERP-View

class BaseMixin(object):
    """
    provides functionality used in EVERY view throughout the application.
    this is used so we don't neet to define a middleware
    """

    def get_permissions(self, permissions):
        """
        returns a list of (django) permissions and use them in dispatch to
        determinate if the user can view the page, he requested
        """
        return permissions


    def check_permissions(self):
        """
        overwrite this function to add a custom permission check (i.e
        one which depends on the object or on the request)
        """
        return True


    def read_session_data(self):
        return self.request.session.get("djangoerp", {'version': get_version()})
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """
        checks permissions, requires a login and
        because we are using a generic view approach to the data-models
        in django ERP, we can ditch a middleware (less configuration)
        and add the functionality to this function.
        """

        if not self.check_permissions() or not self.request.user.has_perms(self.get_permissions([])):
            return permission_denied(self.request)

        # === EMPLOYEE ====================================================

        Employee = get_model_from_cfg('EMPLOYEE')
        if Employee:
            try:
                self.request.djangoerp_employee = Employee.objects.get(user=self.request.user)
            except Employee.DoesNotExist:
                # the user does not have permission to view the erp
                if self.request.user.is_superuser:
                    return redirect('djangoerp:wizard', permanent=False)
                else:
                    raise PermissionDenied
        else:
            self.request.djangoerp_employee = None

        return super(BaseMixin, self).dispatch(*args, **kwargs)


class ViewMixin(BaseMixin):

    def write_session_data(self, data, modify=False):
        # reload sessiondata, because we can not be sure, that the
        # session was not changed during this function (update_notification)
        session_data = self.read_session_data()
        session_data.update(data)

        # update session
        self.request.session["djangoerp"] = session_data
        if modify:
            self.request.session.modified = True

    def get_context_data(self, **kwargs):
        kwargs.update({
            'djangoerp': self.read_session_data()
        })
        # allways read current version, if in development mode
        if settings.DEBUG:
            kwargs["djangoerp"]['version'] = get_version()
        return super(BaseMixin, self).get_context_data(**kwargs)

    def update_notification(self, check_object=True):
        """
        This function is used by django ERP to update the notifications
        used in the ERP-Framework
        """
        if check_object and not self.object.djangoerp_notification.filter(user=self.request.user, unread=True).update(unread=None, changed=now()):
            return None

        # get all session data
        session_data = self.read_session_data()

        # manipulate session
        session_data["notification_last_update"] = datetime.datetime.utcnow().isoformat()
        session_data["notification_count"] = Notification.objects.filter(unread=True, user=self.request.user).count()

        # update session
        self.write_session_data(session_data)


    def update_dashboard(self, pk=None):
        """
        This function is used by django ERP to update the dashboards.
        provide a primary key, if you don't want to set an active
        dashboard.
        """
        session_data = self.read_session_data()
        from .dashboard.models import Dashboard

        session_data["dashboard"] = []
        session_data["dashboard_current"] = None

        update_views = False

        for d in Dashboard.objects.filter(user=self.request.user, name__isnull=False):
            data = {'pk': d.pk, 'name': d.name}
            if pk and int(pk) == d.pk:
                session_data['dashboard_current'] = data
                update_views = True
            session_data['dashboard'].append(data)

        # update session
        self.write_session_data(session_data)

        if update_views:
            self.update_views()

    def update_views(self):
        """
        This function is used by django ERP to update the views.
        just call it, if you need it
        """
        session_data = self.read_session_data()
        from .dashboard.models import View

        # can only be done if a current dashboard is loaded
        if not session_data.get('dashboard_current', None):
            return None
        session_data['views'] = []

        for d in View.objects.filter(dashboard_id=session_data['dashboard_current']['pk']):
            try:
                data = {'pk': d.pk, 'name': d.name, 'category': d.category, 'url': d.get_absolute_url()}
            except NoReverseMatch:
                data = {'pk': d.pk, 'name': d.name, 'category': d.category, 'url': '#'} # TODO 
                continue
            session_data['views'].append(data)

        # update session
        self.write_session_data(session_data)

    def dispatch(self, *args, **kwargs):
        """
        """
        function = super(ViewMixin, self).dispatch(*args, **kwargs)

        if self.request.user.is_anonymous():
            return function

        session_data = self.read_session_data()

        # === NOTIFICATION ================================================

        if 'notification_last_update' in session_data:
            diff = (datetime.datetime.utcnow() - datetime.datetime.strptime(session_data['notification_last_update'], '%Y-%m-%dT%H:%M:%S.%f')).total_seconds()
            if diff >= 300:
                self.update_notification(False)
        else:
            self.update_notification(False)

        # === MESSAGE =====================================================

        session_data["message_count"] = 0

        # === DASHBOARD AND VIEWS =========================================

        if not 'dashboard' in session_data:
            self.update_dashboard()

        return function


class AjaxMixin(BaseMixin):
    """
    add some basic function for ajax requests
    """
    def check_permissions(self):
        return self.request.is_ajax() and super(AjaxMixin, self).check_permissions()

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context, cls=DjangoJSONEncoder)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)


class NextMixin(object):
    """
    redirects to an url or to next, if it is set via get
    """

    def redirect_next(self, reverse, *args, **kwargs):
        redirect_to = self.request.REQUEST.get('next', '')

        netloc = urlparse.urlparse(redirect_to)[1]
        if netloc and netloc != self.request.get_host():
            redirect_to = None

        if redirect_to:
            return redirect_to

        if hasattr(self, 'success_url') and self.success_url:
            return self.success_url

        return reverse_lazy(reverse, args=args, kwargs=kwargs)


# PERMISSIONS

class ModuleViewPermissionMixin(object):
    """
    Checks view permissions of an erpmodule
    """

    def get_permissions(self, perms):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.view_%s' % info)
        return super(ModuleViewPermissionMixin, self).get_permissions(perms)


class ModuleCreatePermissionMixin(object):
    """
    Checks create permissions of an erpmodule
    """

    def get_permissions(self, perms):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.add_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleCreatePermissionMixin, self).get_permissions(perms)


class ModuleClonePermissionMixin(object):
    """
    Checks create permissions of an erpmodule
    """

    def get_permissions(self, perms):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.clone_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleClonePermissionMixin, self).get_permissions(perms)


class ModuleUpdatePermissionMixin(object):
    """
    Checks update permissions of an erpmodule
    """

    def check_permissions(self):
        return self.get_object()._erpworkflow._current_state.update and super(ModuleUpdatePermissionMixin, self).check_permissions()

    def get_permissions(self, perms):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.update_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleUpdatePermissionMixin, self).get_permissions(perms)


class ModuleDeletePermissionMixin(object):
    """
    Checks delete permission of an erpmodule
    """

    def check_permissions(self):
        return self.get_object()._erpworkflow._current_state.delete and super(ModuleDeletePermissionMixin, self).check_permissions()

    def get_permissions(self, perms):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.delete_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleDeletePermissionMixin, self).get_permissions(perms)

# MODULES

class ModuleBaseMixin(object):
    model = None

    def get_object(self):
        if hasattr(self, 'object'):
            return self.object
        return super(ModuleBaseMixin, self).get_object()

    def get_context_data(self, **kwargs):
        ct = ContentType.objects.get_for_model(self.model)
        info = self.model._meta.app_label, self.model._meta.model_name
        kwargs.update({
            'erpmodule': {
                'namespace_index': self.model._erpmeta.url_namespace + ':index',
                'verbose_name_plural': self.model._meta.verbose_name_plural,
                'create_views': self.model._erpmeta.create_views,
                'model': self.model,
                'has_report': self.model._erpmeta.has_report,
                'can_clone': self.model._erpmeta.can_clone and self.request.user.has_perms(['%s.view_%s' % info,'%s.clone_%s' % info,]),
#               'namespace': self.model._erpmeta.url_namespace, #unused
#               'verbose_name': self.model._meta.verbose_name, # unused
            },
        })
        if hasattr(self, 'object') and self.object:
            kwargs.update({
                'erpworkflow': {
                    'enabled': bool(len(self.model._erpworkflow._transitions)),
                    'state': self.object._erpworkflow._current_state,
                    'transitions': self.object._erpworkflow._from_here(),
                },
            })
        return super(ModuleBaseMixin, self).get_context_data(**kwargs)

class ModuleAjaxMixin(ModuleBaseMixin, AjaxMixin):
    """
    base mixin for update, clone and create views (ajax-forms)
    and form-api
    """
    pass


class ModuleViewMixin(ModuleBaseMixin, ViewMixin):
    """
    Basic objects, includes erp-specific functions and context
    variables for erp-views
    """
    pass
