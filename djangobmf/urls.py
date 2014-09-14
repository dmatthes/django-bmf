#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
This is a normal urlconf. it is imported from djangobmf.sites.site.get_url, where
the module views get appended by an '^module/' expression
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.http import last_modified

from djangobmf import get_version
from djangobmf.dashboard.views import DashboardView
from djangobmf.module.views import ModuleView
from djangobmf.modals.views import ModalSaveView


@cache_page(86400, key_prefix='bmf-js18n-%s' % get_version())
@last_modified(lambda req, **kw: timezone.now())
def i18n_javascript(request):
    """
    Displays the i18n JavaScript that the Django admin requires.
    """
    if settings.USE_I18N:  # pragma: no cover
        from django.views.i18n import javascript_catalog
    else:  # pragma: no cover
        from django.views.i18n import null_javascript_catalog as javascript_catalog
    return javascript_catalog(request, packages=['djangobmf'])


urlpatterns = patterns(
    '',
    url(r'^$', DashboardView.as_view(), name="dashboard"),
    url(r'^accounts/', include('djangobmf.account.urls')),
    url(r'^config/', include('djangobmf.configuration.urls')),
    url(r'^dashboard/', include('djangobmf.dashboard.urls')),
    url(r'^document/', include('djangobmf.document.urls')),
    url(r'^i18n/', i18n_javascript, name="jsi18n"),
    #  url(r'^messages/', include('djangobmf.message.urls')),
    url(r'^notifications/', include('djangobmf.notification.urls')),
    url(r'^w/', include('djangobmf.workspace.urls')),
    url(r'^wizard/', include('djangobmf.wizard.urls')),
    #   r'^module/' via sites
    url(r'^modules/$', ModuleView.as_view(), name="modules"),

    # TODO
    url(r'^ajax/save/view/$', ModalSaveView.as_view(), name="modal_saveview"),  # remove me
)
