*****
Model
*****

.. autoclass:: djangoerp.models.ERPSimpleModel
   :members:

.. autoclass:: djangoerp.models.ERPModel
   :members:
   :show-inheritance:

.. autoclass:: djangoerp.models.ERPMPTTModel
   :members:


How to setup an erp-model
===========================================

Create a django model and add the ERPMeta-class to your model:

  class MyModel(models.models):
    myfield = models...

    class ERPMeta:
      pass

Run '''manage.py syncdb''' or '''manage.py migrate''' - that's it.

Options of ERPMeta
------------------------------------------

  has_history = Boolean

If true this module has a history

  allow_comments = Boolean

If true this modules history allows commenting. Needs ``has_history`` enabled. Default: False

  observe_fields = None or List

You can pass a list to this variable. Every change to a fieldname in this list, gets documented in
the models history. Needs ``has_history`` to be enabled. Default: None

  form_class = None

Edit and create Form, default = None


