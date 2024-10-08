from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # driver = fields.Many2one("hr.employee", string="Driver", store=True, readonly=False, tracking=True, required=True)

    # make previous and current balance stored (2/5/2024)#
    current_balance = fields.Float(string="Current Balance", related='partner_id.payment_amount_due', store=True,
                                   readonly=True)

    previous_balance = fields.Float(compute="_compute_total", string="Previous Balance", store=True, readonly=True)
    # ////////////////////////////////////////////////////// #


    @api.depends("amount_total")
    def _compute_total(self):
        for record in self:
                record.previous_balance = record.current_balance - record.amount_total


    # def _prepare_invoice(self):
    #     invoice_vals = super(SaleOrder, self)._prepare_invoice()
    #     invoice_vals['driver'] = self.driver.id
    #     return invoice_vals
