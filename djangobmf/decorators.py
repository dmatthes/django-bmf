#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from functools import wraps
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.encoding import force_str
from django.contrib.auth.views import redirect_to_login

from django.shortcuts import resolve_url
from django.utils.decorators import available_attrs


def login_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks if the user is logged in
    otherwise the user will be redirected to an bmf-login-form
    """
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        return redirect_to_login(
            request.get_full_path(),
            force_str(resolve_url('djangobmf:login')),
            redirect_field_name)
    return wrapped_view
