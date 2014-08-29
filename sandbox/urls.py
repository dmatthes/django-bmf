from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from djangobmf import sites as djangobmf
djangoerp.autodiscover()

from django.views.generic.base import RedirectView

urlpatterns = patterns('',
  url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
)

urlpatterns += i18n_patterns('',
    url(r'^$', RedirectView.as_view(url="/erp/", permanent=False)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bm/', include(djangobmf.site.urls)),
)

if settings.DEBUG or True:
  urlpatterns = patterns('',
     url(r'^erp_documents/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.BMF_DOCUMENT_ROOT, 'show_indexes': True}),
      url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
  ) + urlpatterns
