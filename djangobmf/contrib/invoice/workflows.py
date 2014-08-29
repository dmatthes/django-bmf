#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.workflows import Workflow, State, Transition


class InvoiceWorkflow(Workflow):

    class States:
        draft = State(_(u"Draft"), True, delete=False)
        open = State(_(u"Open"), update=False, delete=False)
        payed = State(_(u"Payed"), update=False, delete=False)
        cancelled = State(_(u"Cancelled"), update=False, delete=True)

    class Transitions:
        send = Transition(_("Send to Customer"), "draft", "open")
        payment = Transition(_("Customer payed"), 'open', 'payed')
        # edit = Transition( _("Edit invoice"), 'open', 'draft')
        cancel = Transition(_("Cancel"), ('draft', 'open'), 'cancelled', validate=False)

    def send(self):
        """
        iterates over each product and generates the transaction for invoice and payment

        the invoice transaction gets directly closed and touches the accounts from the
        customer, products and taxes

        the payment transaction only touches the account from the customer and gets marked as
        a draft
        """
        if not self.instance.transaction:
            transaction_mdl = self.instance._meta.model.transaction.field.related_field.model
            account_mdl = transaction_mdl.accounts.through
            items = self.instance.invoice_products.select_related('product').all()
            transaction = transaction_mdl(
                project=self.instance.project,
                text=self.instance.invoice_number,
                created_by=self.user,
                modified_by=self.user,
            )
            transaction.save()

            # stores informations about the accounts:
            # 0: account_id
            # 1: value
            # 2: Credit (True), Debit(False)
            # 3: Execute transaction
            accounts = []

            for item in items:
                # calculate taxes for the products
                taxes = item.product.calc_tax(item.amount, item.price)
                # add total net to income account (product)
                accounts.append((item.product.income_account_id, taxes[1], True, True))
                for tax, value in taxes[3]:
                    # add taxes
                    accounts.append((tax.account_id, value, True, True))
                # add the gross value to the credit and debit site of the customers liability account
                # and only mark the debit site as executed
                accounts.append((self.instance.project.customer.asset_account_id, taxes[2], False, True))
                accounts.append((self.instance.project.customer.asset_account_id, taxes[2], True, False))

            # sort and summerize the accounts
            credit_execute = {}
            debit_execute = {}
            credit_virtual = {}
            debit_virtual = {}

            for data in accounts:
                if data[2]:
                    if data[3]:
                        arr = credit_execute
                    else:
                        arr = credit_virtual
                else:
                    if data[3]:
                        arr = debit_execute
                    else:  # pragma: no cover
                        # i can't imagine a case where this list is filled
                        arr = debit_virtual
                if data[0] in arr:
                    arr[data[0]] += data[1]
                else:
                    arr[data[0]] = data[1]

            for account, value in credit_execute.items():
                account = account_mdl(
                    account_id=account,
                    transaction=transaction,
                    amount=value,
                    credit=True,
                    balanced=True,
                )
                account.save()
            for account, value in debit_execute.items():
                account = account_mdl(
                    account_id=account,
                    transaction=transaction,
                    amount=value,
                    credit=False,
                    balanced=True,
                )
                account.save()
            for account, value in credit_virtual.items():
                account = account_mdl(
                    account_id=account,
                    transaction=transaction,
                    amount=value,
                    credit=True,
                    balanced=False,
                )
                account.save()
            for account, value in debit_virtual.items():  # pragma: no cover / see above
                account = account_mdl(
                    account_id=account,
                    transaction=transaction,
                    amount=value,
                    credit=False,
                    balanced=False,
                )
                account.save()

            self.instance.transaction = transaction

    def payment(self):
        """
        needs transaction_payment to be "closed" / ballanced
        """
        pass

    def cancel(self):
        """
        needs transaction_payment to be "open"

        it copies the invoice transaction to the payment transaction and marks it as "closed"/ballanced
        """
        pass

# TODO an edit function has to copy the invoice, cancel it, update the related quotation
# (if any) and write a credit note - which is not supported yet
# def edit(self, instance, user):
#   """
#   calls cancel and then resets the invoice and payment transactions
#   """
#   self.cancel(instance, user)
#   instance.transaction_invoice = None
#   instance.transaction_payment = None
