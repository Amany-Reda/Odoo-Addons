from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'


    partner_phone = fields.Char(related='move_id.partner_id.phone' , store=True , readonly=True)

    sales_person= fields.Many2one(related='move_id.partner_id.sales_person', store=True , readonly=True)

    quantity = fields.Float(string="Quantity", default=1)

    price_unit = fields.Float(string="Price Unit")

