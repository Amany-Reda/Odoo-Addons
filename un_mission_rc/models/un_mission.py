from odoo import models, fields,api

class UnMission(models.Model):
    _name = "un.mission"
    _description = "UN Mission"
    _inherit = ["pos.load.mixin"]

    name = fields.Char(required=True)

    un_mission_period = fields.Selection(
        [('month', 'Month'), ('day', 'Day')],
        default='month',
        required=True
    )

    line_ids = fields.One2many(
        'un.mission.line',
        'mission_id',
        string="Category Limits"
    )

    @api.model
    def _load_pos_data_fields(self, config_id):
        return ['id', 'name', 'un_mission_period', 'line_ids']

class UnMissionLine(models.Model):
    _name = "un.mission.line"
    _description = "UN Mission Category Limit"
    _inherit = ["pos.load.mixin"]

    mission_id = fields.Many2one(
        'un.mission',
        required=True,
        ondelete="cascade"
    )

    category_id = fields.Many2one(
        'rc.category',
        required=True
    )

    limit = fields.Float(string="Limit")

    @api.model
    def _load_pos_data_fields(self, config_id):
        return ['id', 'mission_id', 'category_id', 'limit']

