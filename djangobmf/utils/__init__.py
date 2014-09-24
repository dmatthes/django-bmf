#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

__all__ = (
    'generate_filename',
    'get_model_from_name',  # TODO remove me
    'get_model_from_cfg',  # TODO remove me
    'form_class_factory',
)

from .get_model import get_model_from_name  # TODO remove me
from .get_model import get_model_from_cfg  # TODO remove me
from .forms import form_class_factory
