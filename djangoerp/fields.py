#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.six import with_metaclass

from .currency import BaseCurrency

# Workflow
# -----------------------------------------------------------------------------


class WorkflowField(with_metaclass(models.SubfieldBase, models.CharField)):
    """
    Holds the current state of an Workflow object
    can not be edited
    """
    description = _("Workflow object")

    def __init__(self, **kwargs):
        defaults = {
            'max_length': 32, # max length
            'db_index': True,
        }
        defaults.update(kwargs)
        defaults.update({
            'null': True,
            'blank': True,
            'editable': False,
        })
        super(WorkflowField, self).__init__(**defaults)

# Currency and Money
# -----------------------------------------------------------------------------

#lass MoneyFieldProxy(object):
# """
# An equivalent to Django's default attribute descriptor class (enabled via
# the SubfieldBase metaclass, see module doc for details). However, instead
# of callig to_python() on our MoneyField class, it stores the two
# different parts separately, and updates them whenever something is assigned.
# If the attribute is read, it builds the instance "on-demand" with the
# current data.
# (see: http://blog.elsdoerfer.name/2008/01/08/fuzzydates-or-one-django-model-field-multiple-database-columns/)
# """

# def __init__(self, field):
#   self.field = field
#   self.currency_field_name = currency_field_name(self.field.name)

# def _money_from_obj(self, obj):
#   return Money(obj.__dict__[self.field.name], obj.__dict__[self.currency_field_name])

# def __get__(self, obj, type=None):
#   if obj is None:
#     raise AttributeError('Can only be accessed via an instance.')
#   if not isinstance(obj.__dict__[self.field.name], Money):
#     obj.__dict__[self.field.name] = self._money_from_obj(obj)
#   return obj.__dict__[self.field.name]

# def __set__(self, obj, value):
#   if isinstance(value, Money):
#     obj.__dict__[self.field.name] = value.amount
#     setattr(obj, self.currency_field_name, smart_unicode(value.currency))
#   else:
#     if value: value = str(value)
#       obj.__dict__[self.field.name] = self.field.to_python(value)


class MoneyField(with_metaclass(models.SubfieldBase, models.DecimalField)):
    description = _("Money Field")

    def __init__(self, *args, **kwargs):
        defaults = {}
        defaults.update(kwargs)
        defaults.update({
            'max_digits': 27,
            'decimal_places': 9,
        })
        super(MoneyField, self).__init__(*args, **defaults)

    def get_db_prep_save(self, value, *args, **kwargs):
        if isinstance(value, BaseCurrency):
            value = value.value
        return super(MoneyField, self).get_db_prep_save(value, *args, **kwargs)

# def to_python(self, value)


class CurrencyField(with_metaclass(models.SubfieldBase, models.CharField)):
    description = _("Currency Field")

    def __init__(self, *args, **kwargs):
        from .sites import site
        defaults = {
            'max_length': 4, # max length
        }
        defaults.update(kwargs)
        defaults.update({
            'null': True,
            'blank': False,
            'editable': False,
            'default': lambda: site.get_lazy_setting('djangoerp','currency'),
        })
        # TODO using lambda to get the current setting value works, but the function is executed multiple times. maybe a different solution to solve this is better
        super(CurrencyField, self).__init__(*args, **defaults)

    def to_python(self, value):
        if isinstance(value, BaseCurrency):
            return value
        # The string case.
        from .sites import site
        return site.currencies['%s'%value]()

    def get_prep_value(self, value):
        return value.iso
