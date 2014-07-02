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
from django.core.urlresolvers import reverse_lazy

from ..views import AjaxMixin

import urlparse

from .forms import ERPAuthenticationForm

class LogoutModal(AjaxMixin, TemplateView):
    template_name = 'djangoerp/account/modal_logout.html'

class LogoutView(TemplateView):
    template_name = "djangoerp/account/logout.html"

    def get(self, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get(*args, **kwargs)

#from django.shortcuts import redirect


class LoginView(FormView):
    form_class = ERPAuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'djangoerp/account/login.html'

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
#   if self.request.session.test_cookie_worked():
#     self.request.session.delete_test_cookie()
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name, '')
        netloc = urlparse.urlparse(redirect_to)[1]

        if netloc and netloc != self.request.get_host():
            redirect_to = None

        if not redirect_to:
            redirect_to = reverse_lazy('djangoerp:dashboard')
        return redirect_to

# def form_invalid(self, form):
#   self.request.session.set_test_cookie()
#   return super(LoginView, self).form_invalid(form)

# def get(self, request, *args, **kwargs):
#   self.request.session.set_test_cookie()
#   return super(LoginView, self).get(request, *args, **kwargs)
