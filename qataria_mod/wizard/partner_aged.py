from odoo import fields, models, api, _
from odoo.tools.misc import get_lang


class AccountPartnerLedger(models.TransientModel):
    _inherit = "account.aged.trial.balance"

    def _print_report_partner_aged(self, data):
        data = self._get_report_data(data)
        return self.env.ref('qataria_mod.action_report_partner_aged').with_context(landscape=False). \
            report_action(self, data=data)



class AccountCommonReport(models.TransientModel):
    _inherit = "account.common.report"

    def _build_report_contexts(self, data):
        result = {}
        result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['strict_range'] = True if result['date_from'] else False
        result['company_id'] = data['form']['company_id'][0] or False
        return result

    def _print_report_partner_aged(self, data):
        raise NotImplementedError()

    def check_report_partner_aged(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'journal_ids', 'target_move', 'company_id'])[0]
        used_context = self._build_report_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)
        return self.with_context(discard_logo_check=True)._print_report_partner_aged(data)