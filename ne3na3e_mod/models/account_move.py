from odoo import fields, models , api

class AccountMove(models.Model):

    _inherit = 'account.move'

    number_to_words = fields.Char(string="Amount in Words (Total) : ",
                                  compute='_compute_number_to_words',
                                  help="To showing total amount in words")

    def _compute_number_to_words(self):
        """Compute the amount to words in Invoice"""
        for rec in self:
            rec.number_to_words = rec.currency_id.amount_to_text(
                rec.amount_total)
