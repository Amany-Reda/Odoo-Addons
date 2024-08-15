from odoo import models, fields,api

class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].extend(['sales_person'])
        return result




