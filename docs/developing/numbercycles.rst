
Numbercycles
=========================

A numbercycle can be used by any model, which needs a unique automatically generated name (i.e. a quotation)

.. code-block:: python

  from djangoerp.erpcore.numbering.utils import numbercycle_get_name, numbercycle_delete_object

  class MyModel(ERPModel):
    class ERPMeta:
      # activate the cycle with this
      number_cycle = '{counter:01d}'

    # generate a name for every object
    def clear(self):
      if self.name == "":
        self.name = numbercycle_get_name(self)

    # if an object in an active numbering-cycle is deleted, the
    # numbering-cycle should be informed about the action
    def post_delete:
      numbercycle_delete_object(self)

The defintions must contain '{counter:0Nd}' where 'N' is the minmal number of digits the counter should has. The definition
of '{year}' resets the counter every year, while the definition of {month} resets it every month. {month} requires {year}
to be present. By default the numbering cycle uses 'created' to set the time-range.


  




