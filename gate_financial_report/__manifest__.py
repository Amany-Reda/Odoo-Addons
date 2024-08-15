{
    'name': 'Gate Financial Reports',
    'version': '16.0.1.0.10',
    'category': 'Accounting',
    'summary': """Gate Financial Reports with drill 
                down and filters– Community Edition""",
    'description': "Dynamic Financial Reports, DynamicFinancialReports, FinancialReport, Accountingreports, odoo reports, odoo"
                   "This module creates dynamic Accounting General Ledger, Trial Balance, Balance Sheet "
                   "Proft and Loss, Cash Flow Statements, Partner Ledger,"
                   "Partner Ageing, Day book"
                   "Bank book and Cash book reports in Odoo 14 community edition.",

    'author': "Amany Elhwary",
    'Facebook Profile': 'https://www.facebook.com/profile.php?id=100011030985587',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/reports_config_view.xml',
        'report/partner_ledger.xml',
        'report/daybook.xml',
        'report/general_ledger.xml',
        'report/trial_balance.xml',
        'report/ageing.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'gate_financial_report/static/src/css/report.css',
            'gate_financial_report/static/src/js/partner_ledger.js',
            'gate_financial_report/static/src/xml/partner_ledger_view.xml',
            'gate_financial_report/static/src/js/ageing.js',
            'gate_financial_report/static/src/xml/ageing.xml',
            'gate_financial_report/static/src/js/daybook.js',
            'gate_financial_report/static/src/xml/daybook.xml',
            'gate_financial_report/static/src/js/general_ledger.js',
            'gate_financial_report/static/src/xml/general_ledger_view.xml',
            'gate_financial_report/static/src/js/trial_balance.js',
            'gate_financial_report/static/src/xml/trial_balance_view.xml',
        ],
    },
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
