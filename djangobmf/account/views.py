#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from ..viewmixins import AjaxMixin
from ..viewmixins import NextMixin

from .forms import BMFAuthenticationForm


class LogoutModal(AjaxMixin, TemplateView):
    template_name = 'djangobmf/account/modal_logout.html'


class LogoutView(TemplateView):
    template_name = "djangobmf/account/logout.html"

    def get(self, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get(*args, **kwargs)


class LoginView(FormView, NextMixin):
    form_class = BMFAuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'djangobmf/account/login.html'

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            login(self.request, form.get_user())
            return super(LoginView, self).form_valid(form)
        self.request.session.set_test_cookie()
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        return self.redirect_next('djangobmf:dashboard')

    def get(self, request, *args, **kwargs):
        self.request.session.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)
