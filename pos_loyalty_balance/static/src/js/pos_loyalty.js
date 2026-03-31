/** @odoo-module **/
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    setup(vals) {
        // call the original setup
        super.setup(vals);

        // add reactive property
        this.loyalty_points = vals.loyalty_points || 0;
        console.warn('loyalty_points',vals.loyalty_points)
        // add formatted version
        this.loyalty_points_formatted = this.loyalty_points.toFixed(2);
        console.warn('loyalty_points_formatted', this.loyalty_points_formatted);
    },

    setLoyaltyPoints(points) {
        this.loyalty_points = points || 0;
        console.warn('loyalty_points',vals.loyalty_points)
        this.loyalty_points_formatted = this.loyalty_points.toFixed(2);
        console.warn('loyalty_points_formatted', this.loyalty_points_formatted);
    },
    get loyalty_points_currency() {
        if (!this.pos || !this.pos.currency) {
            return this.loyalty_points.toFixed(2);
        }
        // Use POS currency formatting
        return this.pos.currency.format(this.loyalty_points, { digits: 2 });
    },
});