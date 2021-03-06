
from odoo import api, models, fields, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    state = fields.Selection(selection_add=[('cancelled', 'Cancelled')])
    partner_code = fields.Integer(
        related='partner_id.barcode_base', store=True)
    operation_type = fields.Selection([
        ('sepa_debit', 'SEPA Direct Debit'),
        ('sepa_credit', 'SEPA Direct Credit'),
        ('check', 'Check'),
        ('credit_card', 'Credit card'),
        ('lcr', 'LCR'),
        ('other', 'Other')], string='Operation Type')
    text_check_code = fields.Text(string='Check Code')
    text_lcr_code = fields.Text(string='LCR Code')

    @api.onchange('operation_type')
    def onchange_operation_type(self):
        invoice = self.invoice_ids and self.invoice_ids[0] or False
        communication = ''
        if invoice:
            communication = invoice.reference or invoice.name or invoice.number
        if self.operation_type != 'check':
            self.text_check_code = ''
        if self.operation_type != 'lcr':
            self.text_lcr_code = ''
        if self.operation_type == 'sepa_debit':
            self.communication = communication + \
                '-' + _('SEPA Direct Debit')
        if self.operation_type == 'sepa_credit':
            self.communication = communication + \
                '-' + _('SEPA Direct Credit')
        if self.operation_type == 'credit_card':
            self.communication = communication + \
                '-' + _('Credit Card ')
        if self.operation_type == 'other':
            self.communication = communication

    @api.onchange('text_check_code', 'text_lcr_code')
    def onchange_memo_based_on_operation_type(self):
        invoice = self.invoice_ids and self.invoice_ids[0] or False
        communication = ''
        if invoice:
            communication = invoice.reference or invoice.name or invoice.number
        if self.text_check_code:
            check_nb = _('Check nb ')
            self.communication = '%s-%s%s' %\
                (communication, check_nb, self.text_check_code)
        if self.text_lcr_code:
            lcr_nb = _('LCR nb ')
            self.communication = '%s-%s%s' %\
                (communication, lcr_nb, self.text_lcr_code)
