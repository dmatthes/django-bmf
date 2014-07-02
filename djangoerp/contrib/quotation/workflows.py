#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangoerp.workflows import Workflow, State, Transition

import datetime


class QuotationWorkflow(Workflow):
    class States:
        draft = State(_(u"Draft"), True, delete=False)
        send = State(_(u"Send"), update=False, delete=False)
        accepted = State(_(u"Accepted"), update=False, delete=False)
        invoiced = State(_(u"Done"), update=False, delete=False)
        cancelled = State(_(u"Cancelled"), update=False, delete=True)

    class Transitions:
        send = Transition(_("Send to customer"), ["draft"], "send")
        accept = Transition(_("Quotation accepted by customer"), 'send', 'accepted')
        reopen = Transition(_("Reopen this quotation"), 'cancelled', 'draft')
        invoice = Transition(_("Generate invoice"), 'accepted', 'invoiced')
        revise = Transition(_("Revise this quotation"), ('send', 'accepted'), 'draft')
        cancel = Transition(_("Cancel"), ('draft', 'send', 'accepted'), 'cancelled', validate=False)

# def revise(self, instance, user):
#   print instance
#   print user
#   return True

    def invoice(self):
        if not self.instance.invoice:
            Invoice = self.instance._meta.model.invoice.field.related_field.model
            Products = Invoice.products.through
            invoice = Invoice(
                customer=self.instance.customer,
                project=self.instance.project,
                employee=self.instance.employee,
                shipping_address=self.instance.shipping_address,
                invoice_address=self.instance.invoice_address,
                notes=self.instance.notes,
                net=self.instance.net,
                term_of_payment=self.instance.term_of_payment,
                date=datetime.datetime.now().date(),
                created_by=self.user,
                modified_by=self.user,
            )
            invoice.save()

            # save the items from the quotation to the invoice
            for item in self.instance.quotation_products.select_related('product'):
                invoice_item = Products(
                    invoice=invoice,
                    product=item.product,
                    amount=item.amount,
                    price=item.price,
                    name=item.name,
                    description=item.description,
                )
                invoice_item.save()
            self.instance.invoice = invoice
#     self.instance.save()
