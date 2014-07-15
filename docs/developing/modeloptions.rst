=========================
Model ``ERPMeta`` options
=========================

This document explains all the possible 
ERPMeta-options that you can give your model in its internal
``class ERPMeta``.

Available ``ERPMeta`` options
=============================

.. currentmodule:: djangoerp.basemodels

``category``
---------------

Default: ``None``

.. attribute:: Options.category

    Set the name of the Category visible in the Module-overview and within
    the breadcrumb navigation. Django ERP ships with some predefined categories
    in `~djangoerp.categories`

``has_logging``
---------------

Default: ``True``

.. attribute:: Options.has_logging

    If ``has_logging = True``, this model's activity log will
    have entries for created instances and if a instance is changed
    via a workflow transition or the :attr:`~Options.observed_fields` attribute.

``can_clone``
-----------------

Default: ``False``

.. attribute:: Options.can_clone

    Enables if the object can be cloned

``has_comments``
-----------------

Default: ``False``

.. attribute:: Options.has_comments

    Enables comments to models

``has_files``
---------------

Default: ``False``

.. attribute:: Options.has_files

    Enables file-upload to models

``clean``
-------------

Default: ``False``

.. attribute:: Options.clean

    TODO: Explain what this does, why and when you can use this setting

    It has something to do with the model-forms and the saving of data. In some
    special cases the call of an additional clean-method is neccesary. This
    attribute enables the call of an ``erp_clean``-method, which needs to be
    definied at model level

``observed_fields``
-------------------

Default: ``[]`` (Empty list)

.. attribute:: Options.observed_fields

    Only fields definied in this list are checks for changes

``search_fields``
-------------------

Default: ``[]`` (Empty list)

.. attribute:: Options.search_fields

    TODO: Explain the options and give example, what happens if you search an model with an empty list here?

    If a text-search is needed the fields defined here are searched.


``workflow``
-------------------

Default: ``DefaultWorkflow``

.. attribute:: Options.workflow

    TODO: Write doc for workflows and reference it here

    Defines the workflow-object connected to you model


``workflow_field``
-------------------

Default: ``None``

.. attribute:: Options.workflow_field

    If you'd like to store the different workflow-states inside your
    database, you need to tell the model which field is used to store
    the value

        workflow_field = "state"









