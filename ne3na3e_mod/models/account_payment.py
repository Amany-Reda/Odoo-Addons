from odoo import fields, models, api
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = 'account.payment'

    to_verfiy = fields.Boolean('Verfiy', default=False)
    check = fields.Float(string='Check Number' , group_operator=False , digits=(30, 0))
    check_due_date = fields.Date ('Due Date')
    check_value = fields.Monetary(currency_field='currency_id',string='Check Value')
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        compute='_compute_currency_id', store=True, readonly=False, precompute=True,
        help="The payment's currency.")

    @api.constrains('check_due_date')
    def _check_due_date(self):
        for rec in self:
            if not rec.check_due_date and rec.show_partner_bank_account and not rec.is_internal_transfer:
                raise ValidationError("من فضلك أدخل تاريخ الاستحقاق")

    @api.constrains('check_value')
    def _check_check_value(self):
        for rec in self:
            if  rec.show_partner_bank_account and not rec.is_internal_transfer and rec.check_value <= 0:
                raise ValidationError("من فضلك أدخل قيمة الشيك")

    @api.constrains('check')
    def _check_check_length(self):
        for rec in self:
            check_str = str(rec.check)
            if rec.show_partner_bank_account and not rec.is_internal_transfer and len(check_str) < 2:
                raise ValidationError("من فضلك أدخل رقم الشيك")

    @api.depends('journal_id')
    def _compute_currency_id(self):
        for pay in self:
            pay.currency_id = pay.journal_id.currency_id or pay.journal_id.company_id.currency_id
