#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel
from mptt.models import TreeForeignKey

from importlib import import_module


@python_2_unicode_compatible
class Workspace(MPTTModel):
    slug = models.SlugField(max_length=30, blank=False)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        limit_choices_to={'level__lt': 2},
    )
    url = models.CharField(max_length=255, blank=False, editable=False, db_index=True)
    ct = models.ForeignKey(ContentType, related_name="+", on_delete=models.CASCADE, blank=True, null=True)
    # TODO ct should only show bmf modules

    public = models.BooleanField(default=True)
    editable = models.BooleanField(default=True)

    module = models.CharField(max_length=255, blank=True, null=True, editable=True)
#   plugin = models.CharField(max_length=100, blank=False, editable=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

#   class MPTTMeta:
#       order_insertion_by = ['slug']

    class Meta:
        verbose_name = _("Workspace")
        verbose_name_plural = _("Workspace")
        unique_together = (("parent", "slug"), )

    def __str__(self):
        if hasattr(self, 'module_cls') and self.module_cls:
            return '%s' % getattr(self.module_cls, 'name')
        return self.slug

    def __init__(self, *args, **kwargs):
        super(Workspace, self).__init__(*args, **kwargs)
        self.org = self.pk
        self.org_level = self.level

        if self.module:
            module_name, class_name = self.module.rsplit(".", 1)

            try:
                module = import_module(module_name)
            except ImportError:
                # TODO generate warning!
                self.module_cls = None
                return
            self.module_cls = getattr(module, class_name, None)

    def clean(self):
        if self.org:
            if self.parent and self.parent.level != self.org_level - 1:
                raise ValidationError(
                    _("This object's parent must be a %s" % self.parent.type()),
                )
            if not self.parent and self.org_level != 0:
                raise ValidationError(
                    _("This object parent must be a empty"),
                )

        if not self.parent:
            self.ct = None
        else:
            if self.parent.level == 2:
                raise ValidationError(
                    _("You can not append to a %s" % self.parent.type()),
                )
            if self.parent.level == 1:
                if not self.ct:
                    raise ValidationError(
                        _("You need to define a ContentType"),
                    )
                elif not hasattr(self.ct.model_class(), '_bmfmeta'):
                    raise ValidationError(
                        _("The ContentType does not belong to an BMF-Module"),
                    )
            if self.parent.level == 0:
                self.ct = None
        self.update_url()

    def save(self, *args, **kwargs):
        super(Workspace, self).save(*args, **kwargs)
        qs = self.get_children()
        for workspace in qs:
            workspace.update_url()
            workspace.save()

    def type(self):
        if self.level == 2:
            return _('View')
        elif self.level == 1:
            return _('Category')
        return _('Workspace')

    def get_url(self):
        if self.parent:
            return "%s/%s" % (self.parent.url, self.slug)
        else:
            return self.slug

    def update_url(self):
        self.url = self.get_url()

    @models.permalink
    def get_absolute_url(self):
        return ('djangobmf:workspace', (), {"url": self.url})
