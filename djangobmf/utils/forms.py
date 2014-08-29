#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from ..forms import BMFForm


def form_class_factory(cls):
    if issubclass(cls, BMFForm):
        return cls

    class FactoryBMFForm(BMFForm):
        class Meta:
            form_class = cls

    FactoryBMFForm.__name__ = cls.__name__ + str('BMF')
    return FactoryBMFForm
