from odoo import models,api,fields
from datetime import datetime, time

class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        res = super()._load_pos_data_models(config_id)
        res += [
            'un.mission',
            'un.mission.line',
            'rc.category',
        ]
        return res
class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    rc_category_id = fields.Many2one(
        "rc.category",
        string="Ration Control Category",
        index=True,
    )
class PosOrder(models.Model):
    _inherit = "pos.order"

    def _set_rc_category_on_ui_lines(self, order):
        """
        order is the UI dict received from POS.
        Each line is usually like [0, 0, {...vals...}] or [1, id, {...vals...}]
        """
        Product = self.env["product.product"]

        for line_cmd in order.get("lines", []):
            if not isinstance(line_cmd, (list, tuple)) or len(line_cmd) < 3:
                continue

            vals = line_cmd[2] or {}
            product_id = vals.get("product_id")
            if not product_id:
                continue

            product = Product.browse(product_id)
            vals["rc_category_id"] = product.rc_category_id.id or False

    @api.model
    def _process_order(self, order, existing_order):
        self._set_rc_category_on_ui_lines(order)
        return super()._process_order(order, existing_order)

    @api.model
    def get_un_mission_consumed_qty(self, partner_id, mission_id, period="month", exclude_order_id=False):
        if not partner_id or not mission_id:
            return {}

        domain = [
            ("order_id.state", "in", ["paid", "done", "invoiced"]),
            ("order_id.partner_id", "=", partner_id),
            ("order_id.config_id.un_mission_id", "=", mission_id),
            ("rc_category_id", "!=", False),
        ]

        if exclude_order_id:
            domain.append(("order_id", "!=", exclude_order_id))

        today = fields.Date.context_today(self)
        if period == "day":
            start_dt = datetime.combine(today, time.min)
        else:
            start_dt = datetime.combine(today.replace(day=1), time.min)

        domain.append(("order_id.date_order", ">=", start_dt))

        lines = self.env["pos.order.line"].search(domain)

        result = {}
        for line in lines:
            cat_id = line.rc_category_id.id
            result[cat_id] = result.get(cat_id, 0.0) + line.qty

        return result