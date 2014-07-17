#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.datastructures import SortedDict
from django.utils.encoding import python_2_unicode_compatible
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

import inspect
from collections import OrderedDict


@python_2_unicode_compatible
class State(object):
    creation_counter = 0

    def __init__(self, name, default=False, update=True, delete=True, permission=None):
        self.name = name  # name of this state
        self.default = default
        self.update = update  # can update object from this state
        self.delete = delete  # can delete object from this state
        self.permission = permission  # does nothing ... yet!
        self.order = State.creation_counter
        State.creation_counter += 1

    def __str__(self):
        return force_text(self.name)

    def __repr__(self):
        return '<%s: %r>' % (self.__class__.__name__, self.name)


@python_2_unicode_compatible
class Transition(object):
    creation_counter = 0

    def __init__(self, name, sources, target, validate=True, permission=None):
        self.name = name

        if isinstance(sources, six.string_types):
            self.sources = [sources]
        elif hasattr(sources, '__iter__'):
            self.sources = list(sources)
        else:
            # LOOK: you may even add a non-interable object to this dont know why it may be used
            #       maybe it'll be better to raise an acception and accept only
            #       string objects (and even check the iterable object if it returns strings)
            self.sources = [sources]
        self.target = target
        self.validate = validate  # use object validation bevor object is changed
        self.permission = permission  # does nothing ... yet!
        self.order = Transition.creation_counter
        Transition.creation_counter += 1

    def __str__(self):
        return force_text(self.name)

    def __repr__(self):
        return '<%s: %r>' % (self.__class__.__name__, self.name)

    def affected_states(self):
        return self.sources + [self.target]


class WorkflowMetaclass(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(WorkflowMetaclass, cls).__new__
        # six.with_metaclass() inserts an extra class called 'NewBase' in the
        # inheritance tree: Model -> NewBase -> object.
        if name == 'NewBase' and attrs == {}:
            return super_new(cls, name, bases, attrs)

        # excluding Model class itself
        parents = [
                    b for b in bases if
                    isinstance(b, WorkflowMetaclass)
                    and not (b.__name__ == 'NewBase'
                    and b.__mro__ == (b, object))
                  ]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        new_cls = super_new(cls, name, bases, attrs)

        # validation
        if not hasattr(new_cls, 'States'):
            raise ImproperlyConfigured('No states defined in %s' % new_cls)
        if not hasattr(new_cls, 'Transitions'):
            raise ImproperlyConfigured('No transitions defined in %s' % new_cls)

        # set and check states
        new_cls._states = OrderedDict()
        for key, value in sorted(inspect.getmembers(new_cls.States, lambda o: isinstance(o, State)), key=lambda i: i[1].order):
            new_cls._states[key] = value
            if value.default:
                if hasattr(new_cls, '_default_state'):
                    raise ImproperlyConfigured('Two states are defined with an default value in %s' % new_cls)
                else:
                    new_cls._default_state = value
                    new_cls._default_state_key = key
        if len(new_cls._states) == 0:
            raise ImproperlyConfigured('No states defined in %s' % new_cls)
        if not hasattr(new_cls, '_default_state'):
            raise ImproperlyConfigured('You must define a default state in %s' % new_cls)

        # set and check transitions
        new_cls._transitions = OrderedDict()
        for key, value in sorted(inspect.getmembers(new_cls.Transitions, lambda o: isinstance(o, Transition)), key=lambda i: i[1].order):
            if key == "user":
                raise ImproperlyConfigured('The name "user" is reserved, please rename your transition defined in %s' % new_cls)
            if key == "instance":
                raise ImproperlyConfigured('The name "instance" is reserved, please rename your transition defined in %s' % new_cls)
            if key == "set_state":
                raise ImproperlyConfigured('The name "set_state" is reserved, please rename your transition defined in %s' % new_cls)
            for state in value.affected_states():
                if state not in new_cls._states:
                    raise ImproperlyConfigured('The state %s is not defined in %s' % (state, new_cls))
            new_cls._transitions[key] = value

        # autoset transition functions
        for key, value in new_cls._transitions.items():
            if hasattr(new_cls, key):
                continue

            # function template
            def f(self):
                """
                I'm a template-function. Please overwrite me and let me return either None or a (redirect) URL
                """
            setattr(new_cls, key, f)

        # return class
        return new_cls


@python_2_unicode_compatible
class Workflow(six.with_metaclass(WorkflowMetaclass, object)):

    def __init__(self, state=None):
        self.instance = None

        if state:
            self.set_state(state)
        else:
            self._current_state = self._default_state
            self._current_state_key = self._default_state_key
        self._initial_state = self._current_state
        self._initial_state_key = self._current_state_key

    def __str__(self):
        return force_text(self._current_state)

    def _from_here(self):
        out = []
        for key, transition in self._transitions.items():
            if self._current_state_key in transition.sources:
                out.append((key, transition))
        return out

    def set_state(self, key):
        if key not in self._states:
            raise ValidationError(_("The state %s is not valid") % key)
        self._current_state = self._states[key]
        self._current_state_key = key

    def _call(self, key, instance, user):

        # check if key is valid
        if self._current_state_key not in self._transitions[key].sources:
            raise ValidationError(_("This transition is not valid"))

        # update object with instance and user (they come in handy in user-defined functions)
        self.instance = instance
        self.user = user

        # normaly the instance attribute should only be unset during the tests
        if not self.instance:
            self.set_state(self._transitions[key].target)
            return getattr(self, key)()

        # validate the instance
        if self._transitions[key].validate and self._current_state.update:
            self.instance.full_clean()

        # everything is valid, we can set the new state
        self.set_state(self._transitions[key].target)

        # call function
        url = getattr(self, key)()

        # modify and return an redirect url (the instance is not saved here)
        setattr(self.instance, self.instance._erpmeta.workflow_field, self._current_state_key)
        return url


class DefaultWorkflow(Workflow):
    class States:
        default = State('default', default=True, update=True, delete=True)

    class Transitions:
        pass
