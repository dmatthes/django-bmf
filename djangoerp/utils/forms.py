#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from ..forms import ERPForm

def form_class_factory(cls):
    if issubclass(cls, ERPForm):
        return cls

    class FactoryERPForm(ERPForm):
        class Meta:
            form_class = cls

    FactoryERPForm.__name__ = cls.__name__ + str('ERP')
    return FactoryERPForm
