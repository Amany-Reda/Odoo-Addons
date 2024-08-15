{
    'name': 'Ne3na3e Retail Modifications',
    'version': '16.0.0.0',
    'summary': 'Ne3na3e Retail Business module',
    'description': """Custom additions to meet specs of Ne3na3e retail""",
    'author': "Amany Elhwary",
    'Facebook Profile': 'https://www.facebook.com/profile.php?id=100011030985587',
    'images': [
        'static/description/icon.png',
    ],
    'category': 'Accounting',
    'depends': [
        'account',
        'hr',
        'base',
        'point_of_sale',
        'accounting_pdf_reports',
    ],
    'data': [
        'views/account_move_line.xml',
        'views/payment.xml',
        'report/ne3na3e_report.xml',
        'report/partner_aged_report.xml',
        'views/account_move_views.xml',
        'wizard/partner_aged.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'ne3na3e_mod/static/src/js/CustomModels.js',
            'ne3na3e_mod/static/src/js/CustomInvoiceButton.js',
        ]
    },
    'qweb': [],
    'installable': True,
    'application': True,
    'license': 'GPL-3',
    'auto_install': False,
}
