from odoo import models, fields,api

class PosConfig(models.Model):
    _inherit = "pos.config"

    enable_ration = fields.Boolean(string="Enable Ration")
    un_mission_id = fields.Many2one(
        "un.mission",
        string="UN Mission"
    )
    country_id = fields.Many2one(
        "res.country",
        string="Country"
    )

    def _pos_ui_models_to_load(self):
        res = super()._pos_ui_models_to_load()
        res.append('un.mission.line')  # or your model name for ration lines
        return res

    def _pos_ui_fields(self):
        res = super()._pos_ui_fields()
        res.extend(['enable_ration', 'un_mission_id'])
        return res

