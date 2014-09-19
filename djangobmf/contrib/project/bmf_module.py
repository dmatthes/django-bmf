#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import site
from djangobmf.categories import BaseCategory
from djangobmf.categories import ProjectManagement

from .models import Project
from .views import ActiveProjectView
from .views import AllProjectView
from .views import ProjectUpdateView

site.register(Project, **{
    'update': ProjectUpdateView,
})


class ProjectCategory(BaseCategory):
    name = _('Projects')
    slug = "projects"


site.register_dashboard(ProjectManagement)
site.register_category(ProjectManagement, ProjectCategory)
site.register_view(Project, ProjectCategory, ActiveProjectView)
site.register_view(Project, ProjectCategory, AllProjectView)
