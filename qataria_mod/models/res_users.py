# (2/5/2024) restrict on price unit in sale and purchase #
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    readonly_unit_price_sales = fields.Boolean(
        string='Readonly Unit Price for Sales',
        help="This field used to enable readonly or not for sales ")

    readonly_unit_price_purchase = fields.Boolean(
        string='Readonly Unit Price for purchase',
        help="This field used to enable readonly or not for sales ")

    is_admin_boolean = fields.Boolean(compute='_compute_is_admin_boolean')

    def _compute_is_admin_boolean(self):
        """ checks if the currently logged user is admin or not"""
        for rec in self:
            rec.is_admin_boolean = rec.env.user._is_admin()
