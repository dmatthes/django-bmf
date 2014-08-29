*****
Model
*****

.. autoclass:: djangobmf.models.BMFSimpleModel
   :members:

.. autoclass:: djangobmf.models.BMFModel
   :members:
   :show-inheritance:

.. autoclass:: djangobmf.models.BMFMPTTModel
   :members:


How to setup an bmf-model
===========================================

Create a django model and add the BMFMeta-class to your model:

  class MyModel(models.models):
    myfield = models...

    class BMFMeta:
      pass

Run '''manage.py syncdb''' or '''manage.py migrate''' - that's it.

Options of BMFMeta
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


