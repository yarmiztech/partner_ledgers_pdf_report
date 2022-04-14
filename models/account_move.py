
from odoo import fields, models, api,_
from odoo.tools.misc import get_lang



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    branch_id = fields.Many2one("company.branches", string="Branch")
    move_type = fields.Selection(selection=[
        ('entry', 'Journal Entry'),
        ('out_invoice', 'Customer Invoice'),
        ('out_refund', 'Customer Credit Note'),
        ('in_invoice', 'Vendor Bill'),
        ('in_refund', 'Vendor Credit Note'),
        ('out_receipt', 'Sales Receipt'),
        ('in_receipt', 'Purchase Receipt')])
    payment_state = fields.Selection(selection=[
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('reversed', 'Reversed'),
        ('invoicing_legacy', 'Invoicing App Legacy')],
        string="Payment Status", store=True, copy=False, tracking=True,
    )
    def balance_cumulated(self,branch_new,o):
        print(self)
        move_lines = self.env['account.move.line'].search([('partner_id', '=', branch_new.id), ('move_type', '=', 'out_invoice'),
                                              ('account_internal_type', '=', 'receivable')])
        balance = 0
        for each in move_lines:
            check_credit = 0
            check_entry = self.env['account.move'].search(
                [('ref', '=', each.move_id.name), ('move_type', '=', 'entry')]).mapped(
                'line_ids').filtered(lambda a: a.account_internal_type == 'receivable')
            for check in check_entry:
                check_credit += check.credit
            # before = self.env['account.move.line'].search([('id','=',each.id)])
            if o.id >= each.id:
                if o.id == each.id:
                    balance += each.balance
                else:

            # if before in move_lines:
            #     val =
                     balance +=each.balance-check_credit


        # check = self.env['account.move'].search([('ref','=',o.move_id.name),('move_type','=','entry')]).mapped('line_ids').filtered(lambda a:a.account_internal_type == 'receivable')
        # if check:
        return int(balance)

    def balance_before_cumulated(self,branch_new,o):
        print(self)
        # move_lines = self.env['account.move.line'].search([('partner_id', '=', branch_new.id), ('move_type', '=', 'out_invoice'),
        #                                       ('account_internal_type', '=', 'receivable')])
        move_lines = self.env['account.move.line'].search([('partner_id', '=', branch_new.id), ('move_type', '=', 'out_invoice'),
                                              ('account_internal_type', '=', 'receivable')])
        move_lines = branch_new.all_invoices(move_lines)
        balance = 0
        i=0
        if move_lines.filtered(lambda line: line.id < o.id):
            # iter(self.filtered(lambda line: line.balance < 0.0 or line.amount_currency < 0.0))
            # for each in move_lines.filtered(lambda a:a.id < o.id):
            for each in move_lines.filtered(lambda line: line.id < o.id):

                        i+=1
                        mm= move_lines - o

                        check_credit = 0
                        check_entry = self.env['account.move'].search(
                            [('ref', '=',each.move_id.name), ('move_type', '=', 'entry')]).mapped(
                            'line_ids').filtered(lambda a: a.account_internal_type == 'receivable')
                        for check in check_entry:
                            check_credit += check.credit
                        if o.id >= each.id:
                        #     if o.id == each.id:
                        #         balance += each.balance
                        #     else:
                        #     if len(move_lines.filtered(lambda line: line.id < o.id)) == 1:
                        #         balance += each.balance
                        #     else:
                                 balance += each.balance-check_credit
                        if i == len(move_lines.filtered(lambda line: line.id < o.id)):
                            return balance



                # remaining = move_lines-each
                # if remaining:
                #     if o.id <= each.id:
                #         for all in remaining:
                #             if all.id < o.id:
                #                 move_lines = self.env['account.move.line'].search(
                #                     [('partner_id', '=', branch_new.id), ('move_type', '=', 'out_invoice'),
                #                      ('account_internal_type', '=', 'receivable')])
                #                 move_lines = branch_new.all_invoices(move_lines)
                #                 balance = 0
                #                 for each in move_lines:
                #                     check_credit = 0
                #                     check_entry = self.env['account.move'].search(
                #                         [('ref', '=', each.move_id.name), ('move_type', '=', 'entry')]).mapped(
                #                         'line_ids').filtered(lambda a: a.account_internal_type == 'receivable')
                #                     for check in check_entry:
                #                         check_credit += check.credit
                #                     if o.id >= each.id:
                #                         if o.id == each.id:
                #                             balance += each.balance
                #                         else:
                #                             balance += each.balance - check_credit
                #                 return balance
                #     else:
                #         return 0
                # else:
                #     return 0
        # return balance
    def entry_checking(self,o):
       print(o)
       return self.env['account.move'].search([('ref','=',o.move_id.name),('move_type','=','entry')]).mapped('line_ids').filtered(lambda a:a.account_internal_type == 'receivable')
    def entry_checking_credit(self,doc):
        val = 0
        for d in doc:
            val +=sum(self.env['account.move'].search([('ref', '=', d.move_id.name), ('move_type', '=', 'entry')]).mapped('line_ids').filtered(lambda a: a.account_internal_type == 'receivable').mapped('credit'))

        return val

    def balance_received(self,credit,locations):
        if locations:
           return locations-credit
    def balance_received_draft(self,credit,locations):
        if locations:
           return locations-credit
    def balance_cumulated_final(self,branch_new,o):
        final_cal = 0
        final_cal_credit = 0

        for move_debit in self.env['account.move.line'].search([('partner_id', '=', branch_new.id), ('move_type', '=', 'out_invoice'),
                                              ('account_internal_type', '=', 'receivable')]):
            final_cal += move_debit.debit
            for final in move_debit.move_id:
                check_entry = self.env['account.move'].search(
                    [('ref', '=', final.name), ('move_type', '=', 'entry')]).mapped(
                    'line_ids').filtered(lambda a: a.account_internal_type == 'receivable')
                for check in check_entry:
                    final_cal_credit += check.credit
        print(final_cal_credit)
        return  final_cal-final_cal_credit



class AccountMove(models.Model):
    _inherit = 'account.move'

    def all_branch_custom(self):

        for invoices in self.env['account.move'].search([('move_type', '=', 'in_invoice')]):
            for line in invoices.line_ids:
                if invoices.move_type:
                    line.move_type = invoices.move_type
                    line.payment_state = invoices.payment_state
                # else:
                #     line.move_type = 'out_invoice'

    def all_branch_vendor(self):

        for invoices in self.env['account.move'].search([('move_type', '=', 'in_invoice')]):
            for line in invoices.line_ids:
                if invoices.move_type:
                    line.move_type = invoices.move_type
                    line.payment_state = invoices.payment_state
                else:
                    line.move_type = 'in_invoice'

    @api.depends('move_type')
    @api.constrains('move_type')
    def onchange_move_type(self):
        if self.move_type:
            for line in self.invoice_line_ids:
                line.move_type = self.move_type
            for line in self.invoice_line_ids:
                line.move_type = self.move_type
                line.payment_state = self.payment_state
            for line in self.line_ids:
                        line.move_type = self.move_type
                        line.payment_state = self.payment_state

    @api.depends('payment_state','move_type')
    @api.constrains('payment_state','move_type')
    def onchange_payment_state(self):
        for each in self:
            if each.payment_state:
                for line in each.invoice_line_ids:
                    line.payment_state = each.payment_state
            for line in each.invoice_line_ids:
                line.payment_state = each.payment_state
            for line in each.line_ids:
                line.move_type = each.move_type
                line.payment_state = each.payment_state


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def all_invoices(self,docs):
        print('fgf')
        mou = docs.ids
        mou.sort()
        move_lines = self.env['account.move.line']
        for all in mou:
            move_lines += self.env['account.move.line'].browse(all)
        print(move_lines,'move_lines')
        return move_lines

        # docs.sort(lambda a:a.get('Name'))

