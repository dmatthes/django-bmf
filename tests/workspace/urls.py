#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^/', include('djangobmf.workspace.urls', namespace="djangobmf")),
)
