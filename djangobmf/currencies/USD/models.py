#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import site
from djangobmf.currencies import BaseCurrency


class USD(BaseCurrency):
    iso = "USD"
    symbol = _("$")
    name = _("Dollar")

site.register_currency(USD)
