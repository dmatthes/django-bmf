#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import division
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.encoding import force_text
from django.utils.encoding import python_2_unicode_compatible
from django.utils.formats import number_format
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal
from copy import deepcopy


class CurrencyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(CurrencyMetaclass, cls).__new__

        # excluding Model class itself
        parents = [
            b for b in bases if isinstance(b, CurrencyMetaclass)
            and not (b.__name__ == 'NewBase' and b.__mro__ == (b, object))
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
            value = self.name
        else:
            value = self.formatstr % {'val': number_format(self.value, force_grouping=True), 'sym': self.symbol}
        return force_text(value)

    def __repr__(self):
        return force_text("<%s: '%s'>" % (self.__class__.__name__, str(self)))

    # logic .....

    def __bool__(self):
        return bool(self.value)

    def __nonzero__(self):
        return self.__bool__()

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
        raise TypeError("You can not add '%s' to '%s'" % (self.__class__.__name__, other.__class__.__name__))

    def __sub__(self, other):
        """
        should only work with currencies!
        """
        if self.__class__ == other.__class__:
            return self.__class__(self.value - other.value)
        raise TypeError("You can not substract '%s' from '%s'" % (self.__class__.__name__, other.__class__.__name__))

    def __mul__(self, other):
        """
        Multiplication should work with int, float, decimal, but NOT with currency (it makes no sense)
        """
        if isinstance(other, float):
            return self.__class__(Decimal(str(other)) * self.value)
        elif isinstance(other, (six.integer_types, Decimal)):
            return self.__class__(other * self.value)
        raise TypeError("You can not multiply '%s' and '%s'" % (self.__class__.__name__, other.__class__.__name__))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        """
        Division should work with int, float, decimal, returning a currency
        and with Currency returning a decimal
        """
        if isinstance(other, float):
            return self.__class__(self.value // Decimal(str(other)))
        elif isinstance(other, (six.integer_types, Decimal)):
            return self.__class__(self.value // other)
        elif self.__class__ == other.__class__:
            return self.value // other.value
        raise TypeError("You can not divide '%s' by '%s'" % (self.__class__.__name__, other.__class__.__name__))

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
        self._currencies = {}

    def __repr__(self):
        return "<%s object at 0x%x>" % (self.__class__.__name__, id(self))

    def __iter__(self, *args, **kwargs):
        return self._currencies.__iter__(*args, **kwargs)

    def __getitem__(self, key, *args, **kwargs):
        return self._currencies.__getitem__(key, *args, **kwargs)

    def __setitem__(self, key, value, *args, **kwargs):
        return self._currencies.__setitem__(key, value, *args, **kwargs)

    def __bool__(self):
        for key, currency in self.items():
            if currency:
                return True
        return False

    def __nonzero__(self):
        return self.__bool__()

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            keys = list(self.keys())
            for key in other.keys():
                if key not in keys:
                    keys.append(key)
            for key in keys:
                if key not in self and key in other and other[key]:
                    return False  # TODO untested
                if key not in other and key in self and self[key]:
                    return False  # TODO untested
                if key in self and key in other and self[key] != other[key]:
                    return False
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        """
        Addition should only work with currencies!
        """

        if isinstance(other, BaseCurrency):
            wallet = deepcopy(self)
            if other.iso in wallet:
                wallet[other.iso] += other
            else:
                wallet[other.iso] = other
            return wallet

        if isinstance(other, Wallet):
            wallet = deepcopy(self)
            for key, currency in other.items():
                if currency.iso in wallet:
                    wallet[currency.iso] += currency
                else:
                    wallet[currency.iso] = currency
            return wallet

        raise TypeError("Must add a currency or wallet object to the wallet")

    def __sub__(self, other):
        """
        should only work with currencies!
        """

        if isinstance(other, BaseCurrency):
            wallet = deepcopy(self)
            if other.iso in wallet:
                wallet[other.iso] -= other
            else:
                wallet[other.iso] = -1 * other
            return wallet

        if isinstance(other, Wallet):
            wallet = deepcopy(self)
            for key, currency in other.items():
                if currency.iso in wallet:
                    wallet[currency.iso] -= currency
                else:
                    wallet[currency.iso] = -1 * currency
            return wallet

        raise TypeError("Must substract a currency or wallet object from the wallet")

    def __mul__(self, other):
        """
        Multiplication should work with int, float, decimal, but NOT with currency (it makes no sense)
        """
        if isinstance(other, (float, six.integer_types, Decimal)):
            wallet = deepcopy(self)
            for key, currency in wallet.items():
                wallet[key] = other * currency
            return wallet
        raise TypeError(
            "You can not multiply '%s' and '%s'" % (self.__class__.__name__, other.__class__.__name__)
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        """
        Division should work with int, float, decimal, returning a currency
        and with Currency returning a decimal
        """
        if isinstance(other, (float, six.integer_types, Decimal)):
            wallet = deepcopy(self)
            for key, currency in wallet.items():
                wallet[key] = currency // other
            return wallet
        raise TypeError(
            "You can not divide '%s' by '%s'" % (self.__class__.__name__, other.__class__.__name__)
        )

    def items(self, *args, **kwargs):
        return self._currencies.items(*args, **kwargs)

    def keys(self, *args, **kwargs):
        return self._currencies.keys(*args, **kwargs)
