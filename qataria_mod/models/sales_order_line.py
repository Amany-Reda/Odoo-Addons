from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount = fields.Float(string="Discount", digits=(16, 14))
    discount_amount = fields.Float(string="Discount(AMT)", digits=(16, 4))

    @api.depends('product_uom_qty', 'price_unit', 'discount_amount')
    def _compute_amount(self):
        for line in self:
            line.update({
                'price_subtotal': (line.price_unit - line.discount_amount) * line.product_uom_qty,
            })

    @api.onchange("discount")
    def _onchange_discount_percentage(self):
        for line in self:
            if float(line.discount) != 0:
                discount_amount = line.price_unit * float(line.discount) / 100.0
                line.update({"discount_amount": discount_amount})
            if float(line.discount) == 0:
                line.update({"discount_amount": 0.00})
            line._compute_amount()

    @api.onchange("discount_amount")
    def _onchange_discount_amount(self):
        if self.discount_amount > 5.00:
            raise ValidationError("هذا الخصم فوق الحد المسموح به")
        for line in self:
            if line.discount_amount != 0:
                self.discount = 0.0
                if not line.price_unit:
                    raise UserError('Price Unit is Empty')
                if not line.product_uom_qty:
                    raise UserError('Product Quantity is Empty')
                discount = self.discount_amount / self.price_unit * 100 or 0.0
                line.update({"discount": discount})
            if line.discount_amount == 0:
                discount = 0.0
                line.update({"discount": discount})
            line._compute_amount()


    def _prepare_account_move_line(self, move=False):
        self.ensure_one()
        aml_currency = move and move.currency_id or self.currency_id
        date = move and move.date or fields.Date.today()
        res = {
            'display_type': self.display_type or 'product',
            'name': '%s: %s' % (self.order_id.name, self.name),
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': float(self.discount),
            'price_unit': self.currency_id._convert(self.price_unit, aml_currency, self.company_id, date, round=False),
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'purchase_line_id': self.id,
        }
        if self.analytic_distribution and not self.display_type:
            res['analytic_distribution'] = self.analytic_distribution
        return res

    def _prepare_invoice_line(self, **optional_values):
        return super(SaleOrderLine, self)._prepare_invoice_line(
            discount_amount=self.discount_amount,
        )
