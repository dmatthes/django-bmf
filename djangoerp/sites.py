#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.admin.sites import NotRegistered
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import module_has_submodule
from django.utils.module_loading import import_module
from django.utils import six
from django.utils.text import slugify
from django.apps import apps

from .apps import ERPConfig
from .models import Configuration
from .views import ModuleIndexView
from .views import ModuleReportView
from .views import ModuleCreateView
from .views import ModuleDeleteView
from .views import ModuleCloneView
from .views import ModuleAutoDetailView
from .views import ModuleUpdateView
from .views import ModuleWorkflowView
from .views import ModuleFormAPI

import copy

SETTING_KEY = "%s.%s"
APP_LABEL = ERPConfig.label


class DjangoERPSetting(object):
    def __init__(self, app_label, name, field):
        self.app_label = app_label
        self.name = name
        self.field = field

    @property
    def key(self):
        return SETTING_KEY % (self.app_label, self.name)

    @property
    def required(self):
        return self.field.required

    @property
    def changed(self):
        return self.field.initial != self.value

    @property
    def label(self):
        if self.field.label:
            return self.field.label
        return self.key

    @property
    def default(self):
        return self.field.initial

    @property
    def value(self):
        try:
            value = Configuration.objects.get_value(self.app_label, self.name)
        except Configuration.DoesNotExist:
            value = self.field.initial
        return value


class DjangoERPModule(object):
    index = None
    create = None
    delete = None
    update = None
    detail = None
    report = None
    clone = None
    urlpatterns = None

    def __init__(self, model):
        self.model = model

    def get_urls(self, **options):
        index = self.index or options.get('index', None)
        create = self.create or options.get('create', None)
        delete = self.delete or options.get('delete', None)
        update = self.update or options.get('update', None)
        detail = self.detail or options.get('detail', None)
        report = self.report or options.get('report', None)
        clone = self.clone or options.get('clone', None)

        add_patterns = self.urlpatterns or options.get('urlpatterns', None)

        urlpatterns = patterns(
            '',
            url(
                r'^$',
                index.as_view(model=self.model),
                name='index',
            ),
            url(
                r'^(?P<pk>[0-9]+)/$',
                detail.as_view(model=self.model),
                name='detail',
            ),
            url(
                r'^(?P<pk>[0-9]+)/update/$',
                update.as_view(model=self.model),
                name='update',
            ),
            url(
                r'^(?P<pk>[0-9]+)/delete/$',
                delete.as_view(model=self.model),
                name='delete',
            ),
            url(
                r'^(?P<pk>[0-9]+)/update/form-api/$',
                ModuleFormAPI.as_view(
                    model=self.model,
                    form_view=update,
                ),
                name='form-api',
            ),
        )

        # create view(s)
        if isinstance(create, dict):
            for label, view in six.iteritems(create):
                key = slugify(label)
                if isinstance(view, (list, tuple)):
                    label = view[0]
                    view = view[1]
                self.model._erpmeta.create_views.append((key, label))
                urlpatterns += patterns(
                    '',
                    url(
                        r'^create/(?P<key>%s)/$' % key,
                        view.as_view(model=self.model),
                        name='create',
                    ),
                    url(
                        r'^create/(?P<key>%s)/form-api/$' % key,
                        ModuleFormAPI.as_view(
                            model=self.model,
                            form_view=view,
                        ),
                        name='form-api',
                    ),
                )
        else:
            urlpatterns += patterns(
                '',
                url(
                    r'^create/$',
                    create.as_view(model=self.model),
                    name='create',
                ),
                url(
                    r'^create/form-api/$',
                    ModuleFormAPI.as_view(
                        model=self.model,
                        form_view=create,
                    ),
                    name='form-api',
                ),
            )

        # workflow interactions
        if bool(len(self.model._erpworkflow._transitions)):
            urlpatterns += patterns(
                '',
                url(
                    r'^(?P<pk>[0-9]+)/workflow/(?P<transition>\w+)/$',
                    ModuleWorkflowView.as_view(model=self.model),
                    name='workflow',
                ),
            )

        # model reports
        if report:
            self.model._erpmeta.has_report = True
            urlpatterns += patterns(
                '',
                url(
                    r'^(?P<pk>[0-9]+)/report/$',
                    report.as_view(model=self.model),
                    name='report',
                ),
            )

        # clone model
        if self.model._erpmeta.can_clone:
            urlpatterns += patterns(
                '',
                url(
                    r'^(?P<pk>[0-9]+)/clone/$',
                    clone.as_view(model=self.model),
                    name='clone',
                ),
                url(
                    r'^(?P<pk>[0-9]+)/clone/form-api/$',
                    ModuleFormAPI.as_view(
                        model=self.model,
                        form_view=clone,
                    ),
                    name='clone-form-api',
                ),
            )

        # url patterns
        if add_patterns:
            urlpatterns += add_patterns

        return urlpatterns


class DjangoERPSite(object):
    """
    Handle this object like the AdminSite from django.contrib.admin.sites
    """

    def __init__(self, name='djangoerp', app_name=APP_LABEL):
        self.name = name
        self.app_name = app_name
        self.clear()

    def clear(self):
        # combine all registered modules here
        self._registry = {}

        # all currencies should be stored here
        self.currencies = {}

        # all reports should be stored here
        self.reports = {}

        # if a module requires a custom setting, it can be stored here
        self.settings = {}
        self.settings_valid = False
        self.register_settings(APP_LABEL, {
            'company_name': forms.CharField(max_length=100, required=True,),
            'company_email': forms.EmailField(required=True,),
            'currency': forms.CharField(max_length=10, required=True,),  # TODO add validation / use dropdown
        })

    def register(self, model, admin=None, **options):
        self.register_model(model, admin)

        for view in ['index', 'create', 'detail', 'update', 'delete', 'report', 'clone']:
            if view in options:
                self.register_view(model, view, options[view])

        if 'urlpatterns' in options:
            self._registry[model]['urlpatterns'] = options['urlpatterns']

    def register_model(self, model, admin=None):
        if not hasattr(model, '_erpmeta'):
            raise ImproperlyConfigured(
                'The model %s needs to be an ERP-Model in order to be'
                'registered with django ERP.' % model.__name__
            )

        if model in self._registry:
            raise AlreadyRegistered('The model %s is already registered' % model.__name__)

        self._registry[model] = {
            'admin': (admin or DjangoERPModule)(model),
            'index': ModuleIndexView,
            'create': ModuleCreateView,
            'detail': ModuleAutoDetailView,
            'update': ModuleUpdateView,
            'delete': ModuleDeleteView,
            'clone': ModuleCloneView,
            'report': None,
            'urlpatterns': None,
        }

    def unregister(self, model):
        self.unregister_model(model)

    def unregister_model(self, model):
        if model not in self._registry:
            raise NotRegistered('The model %s is not registered' % model.__name__)
        del self._registry[model]

    def register_view(self, model, type, view):
        if type in ['index', 'detail', 'update', 'delete', 'clone']:
            # TODO check if view is an erp-view
            # add the view
            self._registry[model][type] = view

        elif type == 'report':
            if isinstance(view, bool):
                if view:
                    self._registry[model][type] = ModuleReportView
            else:
                # TODO check if view is an erp-view
                # add the view
                self._registry[model][type] = view

        elif type == 'create':
            # if isinstance(create, dict):
            # TODO check if view is an erp-view
            # add the view
            self._registry[model][type] = view

    def register_currency(self, currency):
        if currency.iso in self.currencies:
            raise AlreadyRegistered('The currency %s is already registered' % currency.__name__)
        self.currencies[currency.iso] = currency

    def unregister_currency(self, currency):
        if currency.iso not in self.currencies:
            raise NotRegistered('The currency %s is not registered' % currency.__name__)
        del self.currencies[currency.iso]

    def register_report(self, name, cls):
        if name in self.reports:
            raise AlreadyRegistered('The report %s is already registered' % name)
        self.reports[name] = cls

    def unregister_report(self, name):
        if name not in self.reports:
            raise NotRegistered('The currency %s is not registered' % name)
        del self.reports[name]

    def register_settings(self, app_label, settings_dict):
        for setting_name, options in settings_dict.items():
            self.register_setting(app_label, setting_name, options)

    def register_setting(self, app_label, setting_name, options):
        name = SETTING_KEY % (app_label, setting_name)
        if name in self.settings:
            raise AlreadyRegistered('The setting %s is already registered' % name)
        self.settings[name] = DjangoERPSetting(app_label, setting_name, options)

    def unregister_setting(self, app_label, setting_name):
        name = SETTING_KEY % (app_label, setting_name)
        if name not in self.settings:
            raise NotRegistered('The setting %s is not registered' % name)
        del self.settings[name]

    def check_settings(self):
        self.settings_valid = False
        for key, setting in self.settings:
            if not setting.value and setting.field.required:
                self.settings_valid = False
                return False
        return True

    def get_lazy_setting(self, app_label, setting_name):
        """
        will allways return None, if the django apps are not ready
        """
        if apps.ready:
            return self.get_setting(app_label, setting_name)
        return None

    def get_setting(self, app_label, setting_name):
        name = SETTING_KEY % (app_label, setting_name)
        try:
            return self.settings[name].value
        except KeyError:
            raise NotRegistered('The setting %s is not registered' % name)

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name

    @property
    def models(self):
        models = {}
        for model in self._registry:
            ct = ContentType.objects.get_for_model(model)
            models[ct.pk] = model
        return models

    def check_dependencies(self):
        """
        Check that all things needed to run the admin have been correctly installed.

        The default implementation checks that admin and contenttypes apps are
        installed, as well as the auth context processor.
        """
        if not apps.is_installed('django.contrib.admin'):
            raise ImproperlyConfigured(
                "Put 'django.contrib.admin' in "
                "your INSTALLED_APPS setting in order to use the admin application."
            )
        if not apps.is_installed('django.contrib.contenttypes'):
            raise ImproperlyConfigured(
                "Put 'django.contrib.contenttypes' in "
                "your INSTALLED_APPS setting in order to use the admin application."
            )
        if 'django.contrib.auth.context_processors.auth' not in settings.TEMPLATE_CONTEXT_PROCESSORS:
            raise ImproperlyConfigured(
                "Put 'django.contrib.auth.context_processors.auth' "
                "in your TEMPLATE_CONTEXT_PROCESSORS setting in order to use the admin application."
            )

    def get_urls(self):
        from djangoerp.urls import urlpatterns

        if settings.DEBUG:
            self.check_dependencies()

        for model in self._registry:
            ct = ContentType.objects.get_for_model(model)
            data = self._registry[model]
            urls = data['admin'].get_urls(**{
                "index": data['index'],
                "create": data['create'],
                "detail": data['detail'],
                "update": data['update'],
                "delete": data['delete'],
                "report": data['report'],
                "clone": data['clone'],
                "urlpatterns": data['urlpatterns'],
            })
            info = (model._meta.app_label, model._meta.model_name)
            urlpatterns += patterns(
                '',
                url(
                    r'^module/%s/%s/' % (ct.pk, info[1]),
                    include((urls, self.app_name, "module_%s_%s" % info))
                )
            )
        return urlpatterns

        # Add in each model's views
        for model, model_admin in six.iteritems(self._registry):
            urlpatterns += patterns(
                '',
                url(
                    r'^%s/%s/' % (model._meta.app_label, model._meta.model_name),
                    include(model_admin.urls)
                )
            )

site = DjangoERPSite()


def autodiscover():
    from django.apps import apps

    for app_config in apps.get_app_configs():
        try:
            # get a copy of old site configuration
            before_import_r = copy.copy(site._registry)
            before_import_c = copy.copy(site.currencies)
            before_import_s = copy.copy(site.settings)
            before_import_p = copy.copy(site.reports)
            import_module('%s.%s' % (app_config.name, "erp_module"))
        except:
            # Reset the model registry to the state before the last import
            # skiping this may result in an AlreadyRegistered Error
            site._registry = before_import_r
            site.currencies = before_import_c
            site.settings = before_import_s
            site.reports = before_import_p

            # Decide whether to bubble up this error
            if module_has_submodule(app_config.module, "erp_module"):
                raise
