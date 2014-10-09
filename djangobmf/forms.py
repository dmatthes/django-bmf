#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.forms.fields import FloatField
from django.forms.fields import DecimalField
from django.forms.models import BaseModelFormSet
from django.forms.models import ModelChoiceField
from django.forms.util import ErrorList
from django.utils.encoding import python_2_unicode_compatible
from django.utils import six

from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)


class BMFFormMetaclass(type):
    def __new__(cls, name, bases, attrs):
        new_cls = super(BMFFormMetaclass, cls).__new__(cls, name, bases, attrs)

        meta = attrs.get('Meta', None)
        new_cls.form_class = getattr(meta, 'form_class', None)

        if new_cls.form_class is None:
            return new_cls  # probably a normal formular

        if hasattr(meta, 'inlines'):
            inlines = OrderedDict(
                (prefix, form_class)
                for prefix, form_class in meta.inlines.items()
                if isinstance(form_class, type) and issubclass(form_class, BaseModelFormSet)
            )
        else:
            inlines = OrderedDict()
        new_cls.inlines = inlines
        return new_cls


@python_2_unicode_compatible
class BMFForm(six.with_metaclass(BMFFormMetaclass, object)):

    def __init__(
            self, data=None, files=None, auto_id='bmf_%s', prefix=None,
            initial=None, instance=None, initial_inlines=None,
            error_class=ErrorList, **kwargs):
        self.is_bound = data is not None or files is not None
        self.prefix = prefix or self.get_default_prefix()
        self.auto_id = auto_id
        self.data = data or {}
        self.files = files or {}
        self.initial = initial
        self.error_class = error_class
        self.forms = OrderedDict()
        self._errors = None
        self._non_form_errors = None

        # TODO find out, how this model can get inital values for the related fields
        self.initial_inlines = initial_inlines or {}

        kwargs.update({
            'data': data,
            'files': files,
            'auto_id': self.auto_id,
            'initial': initial,
            'instance': instance,
            'error_class': error_class,
        })

        self.base_form = self.form_class(**self.get_form_kwargs(None, **kwargs))

        # Instantiate all the forms in the container
        for form_prefix, form_class in self.inlines.items():
            inlineform = form_class(
                prefix='-'.join(p for p in [self.prefix, form_prefix] if p),
                **self.get_form_kwargs(form_prefix, **kwargs)
            )
            if form_prefix in self.base_form.fields:
                # update self.forms, make the original field not required and save the required boolean at the formset
                # and mark the field as excluded (otherwise we can't save the instances with inlines), see 'save'-method
                inlineform.required = self.base_form.fields[form_prefix].required
                self.base_form.fields[form_prefix].required = False
                self.base_form.fields[form_prefix].inlineformset = True
                self.forms[form_prefix] = inlineform
                if self.base_form._meta.exclude is None:
                    self.base_form._meta.exclude = [form_prefix]
                else:
                    if form_prefix not in self.base_form._meta.exclude:
                        self.base_form._meta.exclude = tuple(self.base_form._meta.exclude) + (form_prefix,)

    def __str__(self):
        """ Render only the base form ... this should never be used anyway """
        return self.base_form.as_table()

    def __iter__(self):
        """
        iterate only over the base_form, the interesting part is done by getitem and the templatetags
        """
        for name in self.base_form.fields:
            yield self[name]

    def __getitem__(self, name):
        """Return a specific field from the container"""
        return self.base_form[name]

    def clean(self):
        """
        Hook for doing any extra formset-wide cleaning after Form.clean() has
        been called on every form. Any ValidationError raised by this method
        will not be associated with a particular form; it will be accesible
        via formset.non_form_errors()
        """
        pass

    @property
    def errors(self):
        """
        Returns a list of form.errors for every form in self.forms.
        """
        if self._errors is None:
            self.full_clean()
        return self._errors

    def full_clean(self):
        """
        Cleans all of self.data and populates self._errors and self._non_form_errors.
        """
        self._errors = []
        self._non_form_errors = self.error_class()

        if not self.is_bound:  # Stop further processing.
            return

        self._errors.append(self.base_form.errors)
        # TODO make use of min_num in django 1.7+ and delete this code
        try:
            for prefix, formset in self.forms.items():
                self._errors.append(formset.errors)
                if formset.required:
                    c = 0
                    for form in formset:
                        # check if form has a instane OR was changed
                        if form.instance.pk or form.has_changed():  # TODO: check for deletions
                            c += 1
                    # if formset is empty
                    if c == 0:
                        # TODO ... ehmmmm this works, but it's not beautiful
                        msg = 'This formset is required'
                        self.base_form.errors[prefix] = self.error_class([msg])
                        raise ValidationError(msg, code="inline_required")
            # Give self.clean() a chance to do cross-form validation.
            self.clean()
        except ValidationError as e:
            self._non_form_errors = self.error_class(e.error_list)

    def get_all_fields(self):
        """
        Get all the fields in this form
        needed for ajax-interaction (changed value)
        """
        fields = []
        if self.base_form._meta.exclude:
            for field in self:
                if field.name not in self.base_form._meta.exclude:
                    fields.append(field)
        else:
            for field in self:
                fields.append(field)
        for formset in self.forms.values():
            for form in formset:
                for field in form:
                    fields.append(field)
        return fields

    def get_changes(self):
        """
        needed for ajax calls. return fields, which changed between the validation
        """
        # do form validation
        valid = self.is_valid()

        # also do model clean's, which are usually done, if the model is valid
        try:
            self.instance.clean()
            for prefix, formset in self.forms.items():
                for form in formset:
                    form.instance.clean()
        except ValidationError:
            pass

        data = []
        for field in self.get_all_fields():
            # input-type fields
            val_instance = getattr(field.form.instance, field.name, None)

            if isinstance(field.field, (CharField, DecimalField, FloatField)):
                if not field.value() and val_instance:
                    data.append({'field': field.auto_id, 'value': val_instance})
                continue
            if isinstance(field.field, ModelChoiceField):
                try:  # inline formsets cause a attribute errors
                    if val_instance and field.value() != str(val_instance.pk):
                        data.append({'field': field.auto_id, 'value': val_instance.pk, 'name': str(val_instance)})
                except AttributeError:
                    pass
                continue
            logger.critical("Formatting is missing for %s" % field.field.__class__)
        return valid, data

    @classmethod
    def get_default_prefix(cls):
        return 'bmf'

    def get_field(self, auto_id):
        """
        Get the field from the auto_id value of this form
        needed for ajax-interaction (search)
        """
        for field in self:
            if field.auto_id == auto_id:
                return field
        for formset in self.forms.values():
            for form in formset:
                for field in form:
                    if field.auto_id == auto_id:
                        return field
        return None

    def get_form_kwargs(self, prefix, **kwargs):
        """
        overwrite initials for inline forms
        """
        if prefix:
            if prefix in self.initial_inlines:
                kwargs.update({'initial': self.initial_inlines[prefix]})
            else:
                kwargs.update({'initial': {}})
        return kwargs

    @property
    def instance(self):
        return self.base_form.instance

    def is_multipart(self):
        return self.base_form.is_multipart() or any(f.is_multipart() for f in self.forms.values())

    def is_valid(self):
        """
        Returns True if every form in self.forms is valid.
        """
        if not self.is_bound:
            return False
        forms_valid = self.base_form.is_valid()
        # This triggers a full clean.
        self.errors
        # We loop over every form.errors here
        for prefix, form in self.forms.items():
            forms_valid &= form.is_valid()
        return forms_valid and not bool(self.non_form_errors())

    @property
    def media(self):
        all_data = []
        for media in self.base_form.media:
            all_data.append(media)
        for prefix, form in self.forms.items():
            for media in form.media:
                all_data.append(media)
        return all_data

    def non_form_errors(self):
        """
        Returns an ErrorList of errors that aren't associated with a particular
        form.  Returns an empty ErrorList if there are none.
        """
        if self._non_form_errors is None:
            self.full_clean()
        return self._non_form_errors

    def save(self, **kwargs):
        """
        Saves the base form and save subforms, if available
        """
        if len(self.forms) == 0:
            return self.base_form.save(**kwargs)

        if not kwargs.get('commit', True):
            raise ValueError("'%s' object must be commited when saved" % self.__class__.__name__)

        obj = self.base_form.save(**kwargs)  # this can only be done, if the manytomany field is excluded
        for prefix, formset in self.forms.items():
            formset.instance = obj
            formset.save()

        # Rerun model.clean and save the model. So it is possible to write clean methods on an model, which depend
        # on related fields. The usage of these clean methods outside of the bmf is probalby not simple anyway, because
        # they don't need the BMFForm dependency
        if self.instance._bmfmeta.clean:
            obj.bmf_clean()
            obj.save()

        return obj

    # === LOOK AT ===============================================================

    # maybe this is not needed...
    @property
    def cleaned_data(self):
        return self.base_form.cleaned_data

# @property
# def cleaned_data(self):
#   """
#   Returns a list of form.cleaned_data dicts for every form in self.forms.
#   """
#   if not self.is_valid():
#     raise AttributeError("'%s' object has no attribute 'cleaned_data'" % self.__class__.__name__)
#   return [self.base_form.cleaned_data] + [form.cleaned_data for prefix, form in self.forms.items()]
