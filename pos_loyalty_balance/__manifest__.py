{
    "name": "POS Loyalty Card Balance",
    "version": "1.0",
    "summary": "Show customer loyalty card balance on POS receipt",
    "category": "Point of Sale",
    "author": "Your Name",
    "depends": ["point_of_sale", "loyalty",'pos_loyalty'],
    "data": [
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_loyalty_balance/static/src/xml/pos_loyalty_receipt.xml',
            'pos_loyalty_balance/static/src/js/pos_loyalty.js',

        ],
    },

    "installable": True,
    "application": False,
}