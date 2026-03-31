from odoo import models, fields,api

class RcCategory(models.Model):
    _name = "rc.category"
    _description = "RC Category"
    _inherit = ["pos.load.mixin"]

    name = fields.Char(required=True)
    uom_id = fields.Many2one('uom.uom', string="Unit of Measure")

    @api.model
    def _load_pos_data_fields(self, config_id):
        return ['id', 'name']

class ProductTemplate(models.Model):
    _inherit = "product.template"

    rc_category_id = fields.Many2one(
        "rc.category",
        string="Ration Control Category"
    )

class ProductProduct(models.Model):
    _inherit = "product.product"

    rc_category_id = fields.Many2one(
        "rc.category",
        related="product_tmpl_id.rc_category_id",
        store=True,
        readonly=False
    )
    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        if "rc_category_id" not in fields:
            fields.append("rc_category_id")
        return fields


