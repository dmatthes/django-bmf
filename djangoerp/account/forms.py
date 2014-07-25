#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms import TextInput, PasswordInput
from django.utils.translation import ugettext_lazy as _


class ERPAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        usermodel = get_user_model()
        self.username_field = usermodel._meta.get_field(usermodel.USERNAME_FIELD)
        field = self.fields.get('username')
        field.widget = TextInput(attrs={'placeholder': _('Username'), 'class': 'form-control'})
        field = self.fields.get('password')
        field.widget = PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-control'})
