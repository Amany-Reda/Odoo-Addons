# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import fields,api,models

class PosConfig(models.Model):
    _inherit = 'pos.config'
    enable_display_multi_curr = fields.Boolean('Enable Multi Currency',default=True)
    wk_default_currency_id = fields.Many2one('res.currency','Default Currency')
    wk_multi_currency_ids = fields.Many2many(
        "res.currency",relation="disp_res_curr_rel" ,string="Multiple Currencies")
    wk_sel_int_currency = fields.Integer('Selected Currency')
    show_currency_on_product = fields.Boolean('Show currency on Product',default=True)
    show_currency_on_orderline = fields.Boolean('Show currency on Orderline',default=True)
    show_currency_on_total = fields.Boolean('Show currency on Total',default=True)
    show_currency_on_payment_lines = fields.Boolean('Show currency on Payment Lines',default=True)
    show_currency_on_payment_status = fields.Boolean('Enable currency on Payment Status',default=True)

    def set_selected_currency(self,currency_id,config_id):
        config = self.env['pos.config'].browse(config_id)
        config.write({
            'wk_sel_int_currency':currency_id
        })
        return True 

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    pos_wk_default_currency_id = fields.Many2one(related='pos_config_id.wk_default_currency_id', readonly=False)
    pos_enable_display_multi_curr = fields.Boolean(related='pos_config_id.enable_display_multi_curr', readonly=False)
    pos_wk_multi_currency_ids = fields.Many2many(related='pos_config_id.wk_multi_currency_ids', readonly=False)
    pos_show_currency_on_product = fields.Boolean(related='pos_config_id.show_currency_on_product', readonly=False)
    pos_show_currency_on_orderline = fields.Boolean(related='pos_config_id.show_currency_on_orderline', readonly=False)
    pos_show_currency_on_total = fields.Boolean(related='pos_config_id.show_currency_on_total', readonly=False)
    pos_show_currency_on_payment_lines = fields.Boolean(related='pos_config_id.show_currency_on_payment_lines', readonly=False)
    pos_show_currency_on_payment_status = fields.Boolean(related='pos_config_id.show_currency_on_payment_status', readonly=False)

class PosSession(models.Model):
    _inherit = 'pos.session'

    def pos_ui_multi_currencies_data_load(self):
        return self.env['res.currency'].search_read([('id', 'in', self.config_id.wk_multi_currency_ids.ids)],
                                                    ['id','name', 'symbol', 'position',
                                                        'rounding', 'rate', 'decimal_places'],
                                                    )


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    def name_get(self):
        result = []
        for rec in self:
            rate = "{:.3f}".format(rec.rate)
            result.append((rec.id, '%s ( %s )' % (rec.name,rate)))
        return result
