# models/pos_order.py
from odoo import models, fields, api
from datetime import date

class PosOrder(models.Model):
    _inherit = "pos.order"

    loyalty_points = fields.Float(
        "Loyalty Points", digits=(16, 2), compute="_compute_loyalty_points", store=False
    )

    @api.depends("partner_id", "amount_total", "lines")
    def _compute_loyalty_points(self):
        for order in self:
            points = 0.0
            if order.partner_id:
                # Get all active cards
                cards = self.env["loyalty.card"].search([
                    ("partner_id", "child_of", order.partner_id.ids),
                    ("program_id.active", "=", True),
                    "|",
                    ("expiration_date", ">=", date.today()),
                    ("expiration_date", "=", False),
                ])
                points = sum(cards.mapped("points"))

                # Subtract points used in this order (reward lines)
                points_used = sum(order.lines.filtered(
                    lambda l: l.is_reward_line
                ).mapped("points_cost"))

                points -= points_used

            order.loyalty_points = max(points, 0.0)

    def export_for_ui(self, order):
        result = super().export_for_ui(order)
        partner_id = result.get("partner_id")
        points = 0.0
        if partner_id:
            cards = self.env["loyalty.card"].search([
                ("partner_id", "child_of", partner_id),
                ("program_id.active", "=", True),
                "|",
                ("expiration_date", ">=", date.today()),
                ("expiration_date", "=", False),
            ])
            points = sum(cards.mapped("points"))

            points_used = sum(order.lines.filtered(
                lambda l: l.is_reward_line
            ).mapped("points_cost"))

            points -= points_used

        result["loyalty_points"] = max(points, 0.0)
        return result