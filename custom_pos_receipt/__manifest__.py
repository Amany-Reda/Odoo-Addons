{
    'name': 'POS Custom Receipt',
    'category': 'Sales/Point of Sale',
    'summary': 'This module is used to customized receipt of point of sale when a user adds a product in the cart and validates payment and print receipt, then the user can see the client name on POS Receipt. | Custom Receipt | POS Reciept | Payment | POS Custom Receipt',
    'description': "Customized our point of sale receipt",
    'version': '16.0.1.0',
    'website': 'https://www.kanakinfosystems.com',
    'author': 'Kanak Infosystems LLP.',

    'Develop By' :'Amany ElHhwary',
    'Facebook Profile ': 'https://www.facebook.com/profile.php?id=100011030985587',

    'images': ['static/description/banner.jpg'],
    'depends': ['base', 'point_of_sale','hr'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            "custom_pos_receipt/static/src/js/models.js",
            'custom_pos_receipt/static/src/js/PartnerDetailsEditInherit.js',
            "custom_pos_receipt/static/src/xml/pos.xml",
            "custom_pos_receipt/static/src/xml/partner_details.xml",

        ],
    },
    'installable': True,
}
