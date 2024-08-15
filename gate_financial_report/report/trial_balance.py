from odoo import api, models


class TrialBalance(models.AbstractModel):
    _name = 'report.gate_financial_report.trial_balance'

    @api.model
    def _get_report_values(self,docids, data=None):
        if self.env.context.get('trial_pdf_report'):
            if data.get('report_data'):
                data.update({'account_data': data.get('report_data'
                                                      )['report_lines'],
                             'Filters': data.get('report_data')['filters'],
                             'debit_total': data.get('report_data'
                                                     )['debit_total'],
                             'credit_total': data.get('report_data'
                                                      )['credit_total'],
                             'company': self.env.company,
                             })
        return data
