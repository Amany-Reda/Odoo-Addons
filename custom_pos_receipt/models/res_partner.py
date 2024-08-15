from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _category(self):
        return self.env['res.partner.category'].browse(self._context.get('category_id'))

    sales_person = fields.Many2one('res.partner.category','Sales Person', default=_category)

