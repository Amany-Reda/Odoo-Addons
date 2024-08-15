from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    discount = fields.Float(string="Discount", digits=(16, 14))
    discount_amount = fields.Float(string="Discount(AMT)", digits=(16, 4))


    @api.onchange('discount', 'quantity')
    def _onchange_discount_percentage(self):
        for line in self:
            if float(line.discount) != 0:
                discount_amount = line.price_unit * float(line.discount) / 100.0
                line.update({
                    'discount_amount': discount_amount,
                    'price_subtotal': (line.price_unit - line.discount_amount) * line.quantity,
                })
            if float(line.discount) == 0:
                line.update({
                    'discount_amount': 0.00,
                    'price_subtotal': (line.price_unit - line.discount_amount) * line.quantity,
                })

    @api.onchange('discount_amount', 'quantity')
    def _onchange_discount_amount(self):
        if self.discount_amount > 5.00:
            raise ValidationError("هذا الخصم فوق الحد المسموح به")
        for line in self:
            if line.discount_amount != 0:
                self.discount = 0.0
                if not line.price_unit:
                    raise UserError('Price Unit is Empty')
                if not line.quantity:
                    raise UserError('Product Quantity is Empty')
                discount = self.discount_amount / self.price_unit * 100 or 0.0
                line.update({
                    'discount': discount,
                    'price_subtotal': (line.price_unit - line.discount_amount) * line.quantity,
                })
            if line.discount_amount == 0:
                discount = 0.0
                line.update({
                    'discount': discount,
                    'price_subtotal': (line.price_unit - line.discount_amount) * line.quantity,
                })