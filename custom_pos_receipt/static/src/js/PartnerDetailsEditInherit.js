odoo.define("custom_pos_receipt.PartnerDetailsEditInherit", function (require) {
    "use strict";

    const PartnerDetailsEdit = require("point_of_sale.PartnerDetailsEdit");
    const Registries = require("point_of_sale.Registries");
    const { useState } = owl;

    const PartnerDetailsEditInherit = (PartnerDetailsEdit) =>
        class extends PartnerDetailsEdit {
            setup() {
                super.setup();
                const partner = this.props.partner;
                this.changes = useState({
                   ...this.changes,
                    customer_name: partner.customer_name || "",
                });
            }
        };

    Registries.Component.extend('PartnerDetailsEdit', PartnerDetailsEditInherit);

    return PartnerDetailsEditInherit;
});

