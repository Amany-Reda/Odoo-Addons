odoo.define('ne3na3e_mod.CustomModels', function (require) {
    "use strict";

    const PosGlobalState = require('point_of_sale.models').PosGlobalState;
    const Registries = require('point_of_sale.Registries');

    const CustomPosGlobalState = PosGlobalState => class extends PosGlobalState {
        // Add your new method
        get newInvoiceReportAction() {
            return "ne3na3e_mod.Ne3na3eInvoiceReport";
        }
    };

    // Register the extended class
    Registries.Model.extend(PosGlobalState, CustomPosGlobalState);
});
