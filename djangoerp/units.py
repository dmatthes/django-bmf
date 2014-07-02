#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

'''
from __future__ import absolute_import
from __future__ import division

from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.utils import six
#rom django.utils.encoding import force_text
from django.utils.encoding import python_2_unicode_compatible
from django.utils.formats import number_format
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal

class UnitsMetaclass(type):
  def __new__(cls, name, bases, attrs):
    super_new = super(CurrencyMetaclass, cls).__new__
    # six.with_metaclass() inserts an extra class called 'NewBase' in the
    # inheritance tree: Model -> NewBase -> object.
    if name == 'NewBase' and attrs == {}:
      return super_new(cls, name, bases, attrs)

    # excluding Model class itself
    parents = [b for b in bases if 
        isinstance(b, UnitsMetaclass) 
        and not (b.__name__ == 'NewBase' 
        and b.__mro__ == (b, object))
      ]
    if not parents:
      return super_new(cls, name, bases, attrs)

    # Create the class.
    new_cls = super_new(cls, name, bases, attrs)

    # validation
    if not hasattr(new_cls, 'si'):
      raise ImproperlyConfigured('Unit needs an "si" attribute')
    if not hasattr(new_cls, 'name'):
      raise ImproperlyConfigured('Name needs an "name" attribute')
    if not hasattr(new_cls, 'symbol'):
      raise ImproperlyConfigured('Symbol needs an "symbol" attribute')

    # return class
    return new_cls

@python_2_unicode_compatible
class BaseUnit(six.with_metaclass(CurrencyMetaclass, object)):
  formatstr = _('%(val)s %(sym)s')

  def __init__(self, value=None):
    if value:
      self.set(value)
    else:
      self.value = None

  def __str__(self):
    if self.value == None:
      r = self.name
    else:
      r = self.formatstr%{'val': number_format(self.value, force_grouping=True), 'sym': self.symbol }
    return r.encode("utf-8")

  def __repr__(self):
    return "<%s: '%s'>"%(self.__class__.__name__, str(self))

  # logic .....

  def __nonzero__(self):
    return bool(self.value)

# def __lt__(self, other):
#   if self.__class__ == other.__class__:
#     return self.value < other.value
#   raise TypeError("cannot compare '%s' with '%s'"%(self.__class__.__name__,other.__class__.__name__))
# def __le__(self, other):
#   if self.__class__ == other.__class__:
#     return self.value <= other.value
#   raise TypeError("cannot compare '%s' with '%s'"%(self.__class__.__name__,other.__class__.__name__))

# def __gt__(self, other):
#   if self.__class__ == other.__class__:
#     return self.value > other.value
#   raise TypeError("cannot compare '%s' with '%s'"%(self.__class__.__name__,other.__class__.__name__))
# def __ge__(self, other):
#   if self.__class__ == other.__class__:
#     return self.value >= other.value
#   raise TypeError("cannot compare '%s' with '%s'"%(self.__class__.__name__,other.__class__.__name__))

# def __eq__(self, other):
#   if self.__class__ == other.__class__:
#     return self.value == other.value
#   return False
# def __ne__(self, other):
#   return not self.__eq__(other)

  # math .....

# def __add__(self, other):
#   """
#   Addition of currencies ... should only work with currencies!
#   """
#   if self.__class__ == other.__class__:
#     return self.__class__(self.value+other.value)
#   raise TypeError("cannot add '%s' to '%s'"%(self.__class__.__name__,other.__class__.__name__))

# def __sub__(self, other):
#   """
#   Addition of currencies ... should only work with currencies!
#   """
#   if self.__class__ == other.__class__:
#     return self.__class__(self.value-other.value)
#   raise TypeError("cannot substract '%s' from '%s'"%(self.__class__.__name__,other.__class__.__name__))
#
# def __mul__(self, other):
#   """
#   Multiplication should work with int, float, decimal, but NOT with currency (it makes no sense)
#   """
#   if isinstance(other, float):
#     return self.__class__(Decimal(str(other))*self.value)
#   elif isinstance(other, six.integer_types):
#     return self.__class__(other*self.value)
#   elif isinstance(other, Decimal):
#     return self.__class__(other*self.value)
#   raise TypeError("cannot multiply '%s' and '%s'"%(self.__class__.__name__,other.__class__.__name__))
# def __rmul__(self, other):
#   return self.__mul__(other)

# def __floordiv__(self, other):
#   """
#   Division should work with int, float, decimal, returning a currency
#   and with Currency returning a decimal
#   """
#   if isinstance(other, float):
#     return self.__class__(self.value//Decimal(str(other)))
#   elif isinstance(other, six.integer_types):
#     return self.__class__(self.value//other)
#   elif isinstance(other, Decimal):
#     return self.__class__(self.value//other)
#   elif self.__class__ == other.__class__:
#     return self.value//other.value
#   raise TypeError("cannot divide '%s' by '%s'"%(self.__class__.__name__, other.__class__.__name__))

  # functions .....

  def set(self, value):
    if isinstance(value, Decimal):
      self.value = value
    else:
      self.value = Decimal(value)
'''
