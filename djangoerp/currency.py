#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import division
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.formats import number_format
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal
from copy import copy


class CurrencyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(CurrencyMetaclass, cls).__new__
        # six.with_metaclass() inserts an extra class called 'NewBase' in the
        # inheritance tree: Model -> NewBase -> object.
        if name == 'NewBase' and attrs == {}:
            return super_new(cls, name, bases, attrs)

        # excluding Model class itself
        parents = [b for b in bases if
            isinstance(b, CurrencyMetaclass)
            and not (b.__name__ == 'NewBase'
            and b.__mro__ == (b, object))
        ]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        new_cls = super_new(cls, name, bases, attrs)

        # validation
        if not hasattr(new_cls, 'iso'):
            raise ImproperlyConfigured('Currency needs an "iso" attribute')
        if not hasattr(new_cls, 'name'):
            raise ImproperlyConfigured('Currency needs an "name" attribute')
        if not hasattr(new_cls, 'symbol'):
            raise ImproperlyConfigured('Currency needs an "symbol" attribute')
        if not isinstance(new_cls.precision, six.integer_types):
            raise ImproperlyConfigured('The currency precision must be an integer')
        if new_cls.precision < 0:
            raise ImproperlyConfigured('The currency precision must be zero or positive')

        # return class
        return new_cls


@python_2_unicode_compatible
class BaseCurrency(six.with_metaclass(CurrencyMetaclass, object)):
    formatstr = _('%(val)s %(sym)s')
    precision = 2

    def __init__(self, value=None):
        if value:
            self.set(value)
        else:
            self.value = None

    def __str__(self):
        if self.value is None:
            r = self.name
        else:
            r = self.formatstr % {'val': number_format(self.value, force_grouping=True), 'sym': self.symbol}
        return r.encode("utf-8")

    def __repr__(self):
        return "<%s: '%s'>" % (self.__class__.__name__, str(self))

    # logic .....

    def __nonzero__(self):
        return bool(self.value)

    def __lt__(self, other):
        if self.__class__ == other.__class__:
            return self.value < other.value
        raise TypeError("cannot compare '%s' with '%s'" % (self.__class__.__name__, other.__class__.__name__))

    def __le__(self, other):
        if self.__class__ == other.__class__:
            return self.value <= other.value
        raise TypeError("cannot compare '%s' with '%s'" % (self.__class__.__name__, other.__class__.__name__))

    def __gt__(self, other):
        if self.__class__ == other.__class__:
            return self.value > other.value
        raise TypeError("cannot compare '%s' with '%s'" % (self.__class__.__name__, other.__class__.__name__))

    def __ge__(self, other):
        if self.__class__ == other.__class__:
            return self.value >= other.value
        raise TypeError("cannot compare '%s' with '%s'" % (self.__class__.__name__, other.__class__.__name__))

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self.value == other.value
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    # math .....

    def __add__(self, other):
        """
        Addition of currencies ... should only work with currencies!
        """
        if self.__class__ == other.__class__:
            return self.__class__(self.value + other.value)
        raise TypeError("cannot add '%s' to '%s'" % (self.__class__.__name__, other.__class__.__name__))

    def __sub__(self, other):
        """
        should only work with currencies!
        """
        if self.__class__ == other.__class__:
            return self.__class__(self.value - other.value)
        raise TypeError("cannot substract '%s' from '%s'" % (self.__class__.__name__, other.__class__.__name__))

    def __mul__(self, other):
        """
        Multiplication should work with int, float, decimal, but NOT with currency (it makes no sense)
        """
        if isinstance(other, float):
            return self.__class__(Decimal(str(other)) * self.value)
        elif isinstance(other, six.integer_types):
            return self.__class__(other * self.value)
        elif isinstance(other, Decimal):
            return self.__class__(other * self.value)
        raise TypeError("cannot multiply '%s' and '%s'" % (self.__class__.__name__, other.__class__.__name__))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        """
        Division should work with int, float, decimal, returning a currency
        and with Currency returning a decimal
        """
        if isinstance(other, float):
            return self.__class__(self.value // Decimal(str(other)))
        elif isinstance(other, six.integer_types):
            return self.__class__(self.value // other)
        elif isinstance(other, Decimal):
            return self.__class__(self.value // other)
        elif self.__class__ == other.__class__:
            return self.value // other.value
        raise TypeError("cannot divide '%s' by '%s'" % (self.__class__.__name__, other.__class__.__name__))

    # functions .....

    def set(self, value):
        if isinstance(value, Decimal):
            self.value = value
        else:
            self.value = Decimal(value)

        if self.value.as_tuple().exponent > -self.precision:
            self.value = self.value.quantize(Decimal('1E-%s' % self.precision))


class Wallet(object):
    def __init__(self):
        self.currencies = {}

    def __repr__(self):
        return "<%s>" % (self.__class__.__name__)

    def __nonzero__(self):
        for key, currency in self.currencies.items():
            if currency:
                return True
        return False

    def __add__(self, other):
        """
        Addition should only work with currencies!
        """
        if isinstance(other, BaseCurrency):
            wallet = copy(self)
            if other.iso in wallet.currencies:
                wallet.currencies[other.iso] += other
            else:
                wallet.currencies[other.iso] = other
            return wallet
        raise TypeError("Must add a currency to the Wallet")

    def __sub__(self, other):
        """
        should only work with currencies!
        """
        if isinstance(other, BaseCurrency):
            wallet = copy(self)
            if other.iso in wallet.currencies:
                wallet.currencies[other.iso] -= other
            else:
                wallet.currencies[other.iso] = -1 * other
            return wallet
        raise TypeError("Must substract a currency from the Wallet")
