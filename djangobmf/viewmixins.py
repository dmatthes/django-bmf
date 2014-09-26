#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse_lazy
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import get_language
from django.views.decorators.cache import never_cache
from django.views.defaults import permission_denied

from djangobmf import get_version
from djangobmf.decorators import login_required
from djangobmf.models import Notification
from djangobmf.models import Workspace
from djangobmf.utils.user import user_add_bmf

from collections import OrderedDict

import json
import datetime
try:
    from urllib import parse
except ImportError:
    import urlparse as parse

import logging
logger = logging.getLogger(__name__)


class BaseMixin(object):
    """
    provides functionality used in EVERY view throughout the application.
    this is used so we don't neet to define a middleware
    """

    def get_permissions(self, permissions=[]):
        """
        returns a list of (django) permissions and use them in dispatch to
        determinate if the user can view the page, he requested
        """
        return permissions

    def check_permissions(self):
        """
        overwrite this function to add a view permission check (i.e
        one which depends on the object or on the request)
        """
        return True

    def read_session_data(self):
        return self.request.session.get("djangobmf", {'version': get_version()})

    def write_session_data(self, data):
        # reload sessiondata, because we can not be sure, that the
        # session was not changed during this request
        session_data = self.read_session_data()
        session_data.update(data)

        # update session
        self.request.session["djangobmf"] = session_data
        self.request.session.modified = True

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """
        checks permissions, requires a login and
        because we are using a generic view approach to the data-models
        in django BMF, we can ditch a middleware (less configuration)
        and add the functionality to this function.
        """

        if not self.check_permissions() or not self.request.user.has_perms(self.get_permissions([])):
            return permission_denied(self.request)

        # === EMPLOYEE AND TEAMS ==========================================

        user_add_bmf(self.request.user)

        if self.request.user.djangobmf_has_employee and not self.request.user.djangobmf_employee:
            logger.debug("User %s does not have permission to access djangobmf" % self.request.user)
            if self.request.user.is_superuser:
                return redirect('djangobmf:wizard', permanent=False)
            else:
                raise PermissionDenied

        # =================================================================

        return super(BaseMixin, self).dispatch(*args, **kwargs)

    def update_workspace(self, workspace=None):
        """
        This function reads all workspaces for a user instance, builds the
        navigation-tree and updates the active workspace (if neccessary)

        workspace can either be None, the workspaces primary key or None
        """
        cache_key = 'bmf_workspace_%s_%s' % (self.request.user.pk, get_language())
        cache_timeout = 600

        # get navigation key from cache
        data = cache.get(cache_key)
        if not data:
            logger.debug("Reload workspace cache (%s) for user %s" % (cache_key, self.request.user))

            data = {
                "relations": {},
                "dashboards": {},
                "workspace": {},
            }

            cur_dashboard = None
            cur_category = None
            new_category = False
            for ws in Workspace.objects.all():
                if ws.level == 1:
                    cur_category = ws
                    new_category = True
                    continue
                if ws.level == 0:
                    cur_dashboard = ws
                    data['relations'][ws.pk] = (cur_dashboard.pk, None)
                    continue

                model = ws.ct.model_class()
                permissions = ws.module_cls(model=model, workspace=ws).get_permissions([])

                if self.request.user.has_perms(permissions):
                    data['relations'][ws.pk] = (cur_dashboard.pk, cur_category.pk)

                    if cur_dashboard.pk not in data['dashboards'].keys():

                        data['dashboards'][cur_dashboard.pk] = {
                            "url": cur_dashboard.get_absolute_url(),
                            "name": '%s' % cur_dashboard.module_cls.name,
                        }

                        data['workspace'][cur_dashboard.pk] = {
                            "url": cur_dashboard.get_absolute_url(),
                            "name": '%s' % cur_dashboard.module_cls.name,
                            "categories": OrderedDict()
                        }
                    if new_category:
                        data['workspace'][cur_dashboard.pk]["categories"][cur_category.pk] = {
                            "name": '%s' % cur_category.module_cls.name,
                            "views": OrderedDict()
                        }
                        new_category = False
                    data['workspace'][cur_dashboard.pk]["categories"][cur_category.pk]["views"][ws.pk] = {
                        "name": '%s' % ws.module_cls.name,
                        "url": ws.get_absolute_url(),
                    }
            cache.set(cache_key, data, cache_timeout)

        # build current workspace
        if isinstance(workspace, Workspace):
            workspace = workspace.pk

        db, cat = data['relations'].get(workspace, (None, None))
        if cat:
            view = data['workspace'][db]["categories"][cat]["views"][workspace]
        else:
            view = None

        if not db:
            return data["dashboards"], None, None, None, None
        return data["dashboards"], data["workspace"][db], db, workspace, view

    def update_notification(self, count=None):
        """
        This function is used by django BMF to update the notifications
        used in the BMF-Framework
        """
        logger.debug("Updating notifications for %s" % self.request.user)

        # get all session data
        session_data = self.read_session_data()

        # manipulate session
        session_data["notification_last_update"] = datetime.datetime.utcnow().isoformat()
        if count is None:
            session_data["notification_count"] = Notification.objects.filter(
                unread=True,
                user=self.request.user,
            ).count()
        else:
            session_data["notification_count"] = count

        # update session
        self.write_session_data(session_data)


class ViewMixin(BaseMixin):

    def get_context_data(self, **kwargs):

        session_data = self.read_session_data()

        # load the current workspace
        dashboards, workspace, db_active, ws_active, ws_view = self.update_workspace(
            getattr(self, 'workspace', session_data.get('workspace', None))
        )

        # update session
        if db_active and ws_active and session_data.get('dashboard') != db_active \
                or db_active != ws_active and session_data.get('workspace') != ws_active:
            logger.debug("Update session for %s: (dashboard %s->%s) (workspace %s->%s)" % (
                self.request.user,
                session_data.get('dashboard', None),
                db_active,
                session_data.get('workspace', None),
                ws_active,
            ))
            session_data['dashboard'] = db_active
            session_data['workspace'] = ws_active
            self.write_session_data(session_data)

        # update context with session data
        kwargs.update({
            'djangobmf': self.read_session_data(),
            'bmfworkspace': {
                'dashboards': dashboards,
                'workspace': workspace,
                'workspace_active': session_data.get('dashboard', None),
                'dashboard_active': session_data.get('workspace', None),
            },
        })

        # always read current version, if in development mode
        if settings.DEBUG:
            kwargs["djangobmf"]['version'] = get_version()

        return super(ViewMixin, self).get_context_data(**kwargs)


class AjaxMixin(BaseMixin):
    """
    add some basic function for ajax requests
    """
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(AjaxMixin, self).dispatch(*args, **kwargs)

    def check_permissions(self):
        return self.request.is_ajax() and super(AjaxMixin, self).check_permissions()

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context, cls=DjangoJSONEncoder)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def get_ajax_context(self, context):
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super(AjaxMixin, self).render_to_response(context, **response_kwargs)
        response.render()
        ctx = self.get_ajax_context({
            'html': response.rendered_content,
        })
        return self.render_to_json_response(ctx)

    def render_valid_form(self, context):
        ctx = self.get_ajax_context({
            'status': 'valid',
        })
        ctx.update(context)
        return self.render_to_json_response(ctx)


class NextMixin(object):
    """
    redirects to an url or to next, if it is set via get
    """

    def redirect_next(self, reverse=None, *args, **kwargs):
        if 'next' in self.request.REQUEST:
            redirect_to = self.request.REQUEST.get('next', '')

            netloc = parse.urlparse(redirect_to)[1]
            if not netloc or netloc == self.request.get_host():
                return redirect_to

        if hasattr(self, 'success_url') and self.success_url:
            return self.success_url

        if reverse:
            return reverse_lazy(reverse, args=args, kwargs=kwargs)

        return self.request.path_info


# PERMISSIONS

class ModuleViewPermissionMixin(object):
    """
    Checks view permissions of an bmfmodule
    """

    def get_permissions(self, perms=[]):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.view_%s' % info)
        return super(ModuleViewPermissionMixin, self).get_permissions(perms)


class ModuleCreatePermissionMixin(object):
    """
    Checks create permissions of an bmfmodule
    """

    def get_permissions(self, perms=[]):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.add_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleCreatePermissionMixin, self).get_permissions(perms)


class ModuleClonePermissionMixin(object):
    """
    Checks create permissions of an bmfmodule
    """

    def get_permissions(self, perms=[]):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.clone_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleClonePermissionMixin, self).get_permissions(perms)


class ModuleUpdatePermissionMixin(object):
    """
    Checks update permissions of an bmfmodule
    """

    def check_permissions(self):
        return self.get_object()._bmfworkflow._current_state.update \
            and super(ModuleUpdatePermissionMixin, self).check_permissions()

    def get_permissions(self, perms=[]):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.change_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleUpdatePermissionMixin, self).get_permissions(perms)


class ModuleDeletePermissionMixin(object):
    """
    Checks delete permission of an bmfmodule
    """

    def check_permissions(self):
        return self.get_object()._bmfworkflow._current_state.delete \
            and super(ModuleDeletePermissionMixin, self).check_permissions()

    def get_permissions(self, perms=[]):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.delete_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleDeletePermissionMixin, self).get_permissions(perms)


# MODULES

class ModuleBaseMixin(object):
    model = None

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )

        # load employee and team data into user
        user_add_bmf(self.request.user)

        return self.model.has_permissions(queryset, self.request.user)

    def get_object(self):
        if hasattr(self, 'object'):
            return self.object
        return super(ModuleBaseMixin, self).get_object()

    def get_context_data(self, **kwargs):
        info = self.model._meta.app_label, self.model._meta.model_name
        kwargs.update({
            'bmfmodule': {
                'namespace_index': self.model._bmfmeta.url_namespace + ':index',
                'verbose_name_plural': self.model._meta.verbose_name_plural,
                'create_views': self.model._bmfmeta.create_views,
                'model': self.model,
                'has_report': self.model._bmfmeta.has_report,
                'can_clone': self.model._bmfmeta.can_clone and self.request.user.has_perms([
                    '%s.view_%s' % info,
                    '%s.clone_%s' % info,
                ]),
                # 'namespace': self.model._bmfmeta.url_namespace,  # unused
                # 'verbose_name': self.model._meta.verbose_name,  # unused
            },
        })
        if hasattr(self, 'object') and self.object:
            kwargs.update({
                'bmfworkflow': {
                    'enabled': bool(len(self.model._bmfworkflow._transitions)),
                    'state': self.object._bmfworkflow._current_state,
                    'transitions': self.object._bmfworkflow._from_here(self.object, self.request.user),
                },
            })
        return super(ModuleBaseMixin, self).get_context_data(**kwargs)


class ModuleAjaxMixin(ModuleBaseMixin, AjaxMixin):
    """
    base mixin for update, clone and create views (ajax-forms)
    and form-api
    """

    def get_ajax_context(self, context):
        ctx = {
            'object_pk': 0,
            'status': 'ok',  # "ok" for normal html, "valid" for valid forms, "error" if an error occured
            'html': '',
            'message': '',
            'redirect': '',
        }
        ctx.update(context)
        return ctx

    def render_valid_form(self, context):
        context.update({
            'redirect': self.get_success_url(),
        })
        return super(ModuleAjaxMixin, self).render_valid_form(context)


class ModuleViewMixin(ModuleBaseMixin, ViewMixin):
    """
    Basic objects, includes bmf-specific functions and context
    variables for bmf-views
    """
    pass
