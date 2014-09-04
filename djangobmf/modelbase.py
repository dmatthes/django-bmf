#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import signals
from django.db.models.base import ModelBase
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.fields import GenericRelation

from .apps import BMFConfig

from .workflows import DefaultWorkflow
from .fields import WorkflowField

from .activity.models import Activity
from .notification.models import Notification

import types
import inspect

from mptt.managers import TreeManager
from mptt.models import MPTTModelBase, MPTTModel

APP_LABEL = BMFConfig.label


def add_signals(cls):
    # cleanup history and follows
    def post_delete(sender, instance, *args, **kwargs):
        Activity.objects.filter(
            parent_ct=ContentType.objects.get_for_model(sender),
            parent_id=instance.pk,
        ).delete()
        Notification.objects.filter(
            watch_ct=ContentType.objects.get_for_model(sender),
            watch_id=instance.pk,
        ).delete()
    signals.post_delete.connect(post_delete, sender=cls, weak=False)


# TODO:
# we should create a workflow-enabled model with a fixes workflow field (also in db) and skip the
# probably unneccesary options

# TODO:
# we also should move the "permission" to an bmfacl manager to access the queryset
# from related objects


class BMFOptions(object):
    """
    Options class for BMF models. Use this as an inner class called ``BMFMeta``::

      class MyModel(BMFModel):
        class BMFMeta:
          category = 'mycategory'
    """

    def __init__(self, cls, meta, options=None):

        # overwriteable =========================================================
        self.category = _("No category")
        self.has_logging = True
        self.has_comments = False
        self.has_files = False
        self.can_clone = False
        self.clean = False
        self.observed_fields = []
        self.search_fields = []
        self.number_cycle = None
        self.workflow = DefaultWorkflow
        self.workflow_field = None

        # protected =============================================================
        # used to detect changes
        self.changelog = {}
        # set namespace of urls
        self.url_namespace = '%s:module_%s_%s' % (APP_LABEL, meta.app_label, meta.model_name)
        # is set to true if a report-view is defined for this model (see sites.py)
        self.has_report = False
        # is filles with keys if multiple create views are definied for this model (see sites.py)
        self.create_views = []

        if options:
            options = inspect.getmembers(cls.BMFMeta)
        else:
            options = []

        # set options
        for key, value in options:
            # auto-set known options (no validation!)
            if key in [
                'category',
                'has_logging',
                'has_comments',
                'has_files',
                'search_fields',
                'number_cycle',
                'workflow',
                'workflow_field',
                'clean',
                'can_clone',
            ]:
                setattr(self, key, value)

            # only observe valid fields
            if key == "observed_fields":
                for field in meta.local_fields:
                    if not field.rel and field.name in value \
                            and field.name not in ['created', 'modified', 'created_by', 'modified_by']:
                        self.observed_fields.append(field.name)

        # determin if the model has an workflow
        self.has_workflow = bool(self.workflow_field) and self.has_logging

        # determin if the model detects changes
        self.has_detectchanges = bool(self.observed_fields) and self.has_logging

        # determin if the model can be watched by a user
        self.has_watchfunction = self.has_workflow or self.has_detectchanges \
            or self.has_comments or self.has_files

        # determin if the model has an activity
        self.has_activity = self.has_logging or self.has_comments or self.has_files

        self.has_history = self.has_logging  # TODO OLD REMOVE ME


class BMFModelBase(ModelBase):
    """
    Metaclass for BMF models
    """

    def __new__(cls, name, bases, attrs):
        cls = super(BMFModelBase, cls).__new__(cls, name, bases, attrs)

        parents = [b for b in bases if isinstance(b, BMFModelBase)]
        if not parents:
            # If this is the ModelBase-Class itself - do nothing
            return cls
        if cls._meta.abstract:
            # Don't do anything on abstract models
            return cls

        # make bmf-attributes
        cls._bmfmeta = BMFOptions(cls, cls._meta, getattr(cls, 'BMFMeta', None))

        if type(cls._meta.permissions) is not tuple:
            cls._meta.permissions = tuple(cls._meta.permissions)

        # generate permissions
        cls._meta.permissions += (
            ('view_' + cls._meta.model_name, u'Can view %s' % cls.__name__),
        )
        if cls._bmfmeta.can_clone:
            cls._meta.permissions += (
                ('clone_' + cls._meta.model_name, u'Can clone %s' % cls.__name__),
            )
        if cls._bmfmeta.has_comments:
            cls._meta.permissions += (
                ('comment_' + cls._meta.model_name, u'Can comment on %s' % cls.__name__),
            )
        if cls._bmfmeta.has_files:
            cls._meta.permissions += (
                ('addfile_' + cls._meta.model_name, u'Can add files to %s' % cls.__name__),
            )

        # make workflow
        cls._bmfworkflow = cls._bmfmeta.workflow()
        if cls._bmfmeta.has_workflow:
            try:
                if not isinstance(cls.__dict__[cls._bmfmeta.workflow_field].field, WorkflowField):
                    raise ImproperlyConfigured(
                        '%s is not a WorkflowField in %s' % (
                            cls._bmfmeta.workflow_field, cls._meta.model.__class__.__name__
                        )
                    )
            except KeyError:
                raise ImproperlyConfigured(
                    '%s is not a WorkflowField in %s' % (
                        cls._bmfmeta.workflow_field, cls._meta.model.__class__.__name__
                    )
                )

        if cls._bmfmeta.clean:
            if not hasattr(cls, 'bmf_clean') and not cls._meta.abstract:
                raise ImproperlyConfigured('%s has not a bmf_clean method' % (cls.__name__))

        # add history signals for this model
        add_signals(cls)

#       # add signals from base-classes
#       if hasattr(cls,'pre_save'):
#           if isinstance(cls.pre_save, types.FunctionType):
#               signals.pre_save.connect(cls.pre_save, sender=cls, weak=False)

#       if hasattr(cls,'post_init'):
#           if isinstance(cls.post_init, types.FunctionType):
#               signals.post_init.connect(cls.post_init, sender=cls, weak=False)

        if hasattr(cls, 'post_save'):
            """
            @staticmethod
            def post_save(sender, instance, created, raw, *args, **kwargs):
              pass
            """
            if isinstance(cls.post_save, types.FunctionType):
                signals.post_save.connect(cls.post_save, sender=cls, weak=False)

        if hasattr(cls, 'post_delete'):
            """
            @staticmethod
            def post_delete(sender, instance, *args, **kwargs):
              pass
            """
            if isinstance(cls.post_delete, types.FunctionType):
                signals.post_delete.connect(cls.post_delete, sender=cls, weak=False)

        return cls


class BMFSimpleModel(six.with_metaclass(BMFModelBase, models.Model)):
    """
    Base class for BMF models.
    """
    modified = models.DateTimeField(_("Modified"), auto_now=True, editable=False, null=True, blank=False)
    created = models.DateTimeField(_("Created"), auto_now_add=True, editable=False, null=True, blank=False)
    modified_by = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        null=True, blank=True, editable=False,
        related_name="+", on_delete=models.SET_NULL)
    created_by = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        null=True, blank=True, editable=False,
        related_name="+", on_delete=models.SET_NULL)
    djangobmf_activity = GenericRelation(Activity, content_type_field='parent_ct', object_id_field='parent_id')
    djangobmf_notification = GenericRelation(Notification, content_type_field='watch_ct', object_id_field='watch_id')

    class Meta:
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'view')

    def __init__(self, *args, **kwargs):
        super(BMFSimpleModel, self).__init__(*args, **kwargs)
        # update the state of the workflow with object data
        if self._bmfmeta.workflow_field:
            if hasattr(self, self._bmfmeta.workflow_field):
                self._bmfworkflow = self._bmfmeta.workflow(getattr(self, self._bmfmeta.workflow_field))
                if getattr(self, self._bmfmeta.workflow_field) is None:
                    # set default value in new objects
                    setattr(
                        self,
                        self._bmfmeta.workflow_field,
                        self._bmfworkflow._current_state_key
                    )
        if self.pk and len(self._bmfmeta.observed_fields) > 0:
            self._bmfmeta.changelog = self._get_observed_values()

    def _get_observed_values(self):
        """
        returns the values of every field in self._bmfmeta.observed_fields as a dictionary
        """
        return dict([(field, getattr(self, field)) for field in self._bmfmeta.observed_fields])

    def get_workflow_state(self):
        """
        Returns the current state of the workflow attached to this model
        """
        return self._bmfworkflow._current_state

    @classmethod
    def has_permissions(cls, qs, user):  # DRAFT!!
        """
        Overwrite this function to enable object bases permissions. It must return
        a queryset.

        Default: queryset
        """
        return qs

    def bmfget_project(self):
        """
        The result of this value is currently used by the document-management system
        to connect the file uploaded to this model with a project instance

        Default: None
        """
        return None

    def bmfget_customer(self):
        """
        The result of this value is currently used by the document-management system
        to connect the file uploaded to this model with a customer instance

        Default: None
        """
        return None

    @models.permalink
    def bmfmodule_detail(self):
        """
        A permalink to the default view of this model in the BMF-System
        """
        return ('%s:detail' % self._bmfmeta.url_namespace, (), {"pk": self.pk})

    def get_absolute_url(self):
        return self.bmfmodule_detail()


class BMFModel(BMFSimpleModel):
    """
    BMFModel with uuid. A uuid is used to identify an entry in an syncronisation
    """
    uuid = models.CharField("UUID", max_length=100, null=True, blank=True, editable=False, db_index=True)

    class Meta:
        abstract = True


class BMFMPTTModelBase(MPTTModelBase, BMFModelBase):
    pass


class BMFMPTTModel(six.with_metaclass(BMFMPTTModelBase, BMFModel, MPTTModel)):
    objects = TreeManager()

    class Meta:
        abstract = True
