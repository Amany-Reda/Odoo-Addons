{
    "name": "UN Mission RC",
    "version": "1.0",
    "author": "Amany ElHwary",
    "support": "redaelhwary235@gmail.com",
    "summary": "UN Mission Ration Control for POS",
    "description": """
        UN Mission POS Ration Control Module

        Developer: Amany ElHwary
        Email: redaelhwary235@gmail.com
        Phone: 01095562626
    """,

    "depends": ["sale", "uom", "sales_team", "point_of_sale"],

    "data": [
        "security/ir.model.access.csv",
        "views/pos_config_views.xml",
        "views/rc_category_views.xml",
        "views/un_mission_views.xml",
        "views/menu.xml",
    ],

    "assets": {
        "point_of_sale._assets_pos": [
            "un_mission_rc/static/src/xml/pos_receipt.xml",
            "un_mission_rc/static/src/js/receipt_screen.js",
            # "un_mission_rc/static/src/js/ration_limit.js",
        ],
    },

    "installable": True,
    "application": False,
}