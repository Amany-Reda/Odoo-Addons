from odoo import _, api, fields, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    expiration_date = fields.Datetime(
        string='Expiration Date', related='lot_id.expiration_date', store=True, readonly=True,
        help='This is the date on which the goods with this Serial Number may become dangerous and must not be consumed.')

