#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.six import with_metaclass

from .currency import BaseCurrency


class WorkflowField(with_metaclass(models.SubfieldBase, models.CharField)):
    """
    Holds the current state of an Workflow object
    can not be edited
    """
    description = _("Workflow object")

    def __init__(self, **kwargs):
        defaults = {
            'max_length': 32,  # max length
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
# see: http://blog.elsdoerfer.name/2008/01/08/fuzzydates-or-one-django-model-field-multiple-database-columns/


def get_default_currency():
    from .sites import site
    return site.get_lazy_setting('djangobmf', 'currency')


class MoneyProxy(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        return obj.__dict__[self.field.name].value

    def __set__(self, obj, value):
        currency = getattr(obj, self.field.get_currency_field_name())

        if self.field.has_precision:
            precision = getattr(obj, self.field.get_precision_field_name())
        else:
            precision = 0

        if not isinstance(value, BaseCurrency):
            value = currency.__class__(value, precision=precision)

        obj.__dict__[self.field.name] = value


class CurrencyField(with_metaclass(models.SubfieldBase, models.CharField)):
    description = _("Currency Field")

    def __init__(self, *args, **kwargs):
        defaults = {
            'max_length': 4,
            'editable': False,
        }
        defaults.update(kwargs)
        defaults.update({
            'null': True,
            'blank': False,
            'default': get_default_currency,
        })
        super(CurrencyField, self).__init__(*args, **defaults)

    def to_python(self, value):
        if isinstance(value, BaseCurrency):
            return value
        # The string case.
        from .sites import site
        return site.currencies['%s' % value]()

    def get_prep_value(self, obj):
        if hasattr(obj, 'iso'):
            return obj.iso
        return None

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)


class MoneyField(models.DecimalField):
    description = _("Money Field")

    def __init__(self, *args, **kwargs):
        defaults = {
            'default': '0',
            'blank': True,
        }
        defaults.update(kwargs)
        defaults.update({
            'null': True,
            'max_digits': 27,
            'decimal_places': 9,
        })
        super(MoneyField, self).__init__(*args, **defaults)

    def to_python(self, value):
        if isinstance(value, BaseCurrency):
            return value.value
        return super(MoneyField, self).to_python(value)

    def get_currency_field_name(self):
        return '%s_currency' % self.name

    def get_precision_field_name(self):
        return '%s_precision' % self.name

    def contribute_to_class(self, cls, name):
        super(MoneyField, self).contribute_to_class(cls, name)
        if not cls._meta.abstract:
            self.has_precision = hasattr(self, self.get_precision_field_name())
            setattr(cls, self.name, MoneyProxy(self))

    def get_prep_value(self, value):
        if isinstance(value, BaseCurrency):
            value = value.value
        super(MoneyField, self).get_prep_value(value)

    def get_db_prep_save(self, value, *args, **kwargs):
        if isinstance(value, BaseCurrency):
            value = value.value
        return super(MoneyField, self).get_db_prep_save(value, *args, **kwargs)
