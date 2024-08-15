{
    'name': 'POS Automate Invoice',
    'version': '16.0.1.0.0',
    'summary': """To manage the POS Invoice Automatically""",
    'description': """This module facilitates the automated sending of invoices
     to customers, along with the ability to schedule emails at specific 
     intervals. Additionally, it empowers users to download invoices 
     based on predefined conditions within the configuration settings.""",
    'category': 'Sales',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',

    'Develop By': 'Amany ElHhwary',
    'Facebook Profile ': 'https://www.facebook.com/profile.php?id=100011030985587',

    
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['account', 'point_of_sale','ne3na3e_mod'],
    'website': 'https://www.cybrosys.com',
    'data': [
        'data/send_mail_template.xml',
        'data/send_mail_cron.xml',
        'views/res_config_settings.xml',
        'views/pos_order.xml',
        'views/pos_config.xml',
        'views/ir_cron.xml'
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_invoice_automate/static/src/js/PaymentScreen.js',
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
