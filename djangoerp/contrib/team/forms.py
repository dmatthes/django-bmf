#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm

from djangoerp.forms import ERPForm

from .models import Team
# from .models import TeamMember


class TeamUpdateForm(ModelForm):
    class Meta:
        model = Team
        exclude = []


class TeamCreateForm(ModelForm):
    class Meta:
        model = Team
        exclude = []

# TeamInlineFormset = inlineformset_factory(Team, TeamMember, extra=1, exclude=[])


class ERPTeamUpdateForm(ERPForm):
    class Meta:
        form_class = TeamUpdateForm
        # inlines = {'members': TeamInlineFormset}


class ERPTeamCreateForm(ERPForm):
    class Meta:
        form_class = TeamCreateForm
        # inlines = {'members': TeamInlineFormset}
