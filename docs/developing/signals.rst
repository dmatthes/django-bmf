
**************
Signals
**************

A list of all the signals than django BMF sends.

activity_create
---------------

.. data:: djangobmf.signals.activity_create
   :module:

This signal is send, when an BMF model is created.

Arguments sent with this signal:

``sender``
    As above: the model class that just had an instance created.

``instance``
    The actual instance of the model that's just been created.


activity_update
---------------

.. data:: djangobmf.signals.activity_update
   :module:

This signal is send, when an BMF model has detected changes in observed fields.

Arguments sent with this signal:

``sender``
    As above: the model class that just had an instance created.

``instance``
    The actual instance of the model that's just been created.



activity_comment
----------------

.. data:: djangobmf.signals.activity_comment
   :module:

This signal is send, when a comment is written on a module.

Arguments sent with this signal:

``sender``
    As above: the model class that just had an instance created.

``instance``
    The actual instance of the model that's just been created.



activity_addfile
----------------

.. data:: djangobmf.signals.activity_addfile
   :module:

This signal is send, when a file is added to a module.

Arguments sent with this signal:

``sender``
    As above: the model class that just had an instance created.

``instance``
    The actual instance of the model that's just been created.

``file``
    The file instance, that was just uploaded.



activity_workflow
-----------------

This signal is send, when the models workflow state was changed.

.. data:: djangobmf.signals.activity_workflow
   :module:

Arguments sent with this signal:

``sender``
    As above: the model class that just had an instance created.

``instance``
    The actual instance of the model that's just been created.
