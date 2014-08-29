#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from djangobmf.forms import BMFForm

from .models import Team
from .models import TeamMember


class TeamUpdateForm(ModelForm):
    class Meta:
        model = Team
        exclude = []


class TeamCreateForm(ModelForm):
    class Meta:
        model = Team
        exclude = []

TeamInlineFormset = inlineformset_factory(Team, TeamMember, extra=2, exclude=[])


class BMFTeamUpdateForm(BMFForm):
    class Meta:
        form_class = TeamUpdateForm
        inlines = {'members': TeamInlineFormset}


class BMFTeamCreateForm(BMFForm):
    class Meta:
        form_class = TeamCreateForm
        inlines = {'members': TeamInlineFormset}
