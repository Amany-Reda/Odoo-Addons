from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"
    # _order = 'sequence, id'

    del_partner_id = fields.Many2one(related='picking_id.partner_id')
