/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

function getId(value) {
    if (!value) return false;
    if (Array.isArray(value)) return value[0];
    if (typeof value === "object" && "id" in value) return value.id;
    return value;
}

function getModelRecords(pos, modelName) {
    const model = pos.models?.[modelName];
    if (!model) return [];
    if (typeof model.getAll === "function") return model.getAll();
    if (model.records) return Object.values(model.records);
    return [];
}

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        const order = this.currentOrder;
        const pos = this.pos;
        const config = pos.config;

        if (!config.enable_ration) {
            return super.validateOrder(...arguments);
        }

        const missionId = getId(config.un_mission_id);
        const partner = order.getPartner();
        const partnerId = partner?.id;

        if (!missionId) {
            return super.validateOrder(...arguments);
        }

        if (!partnerId) {
            this.dialog.add(AlertDialog, {
                title: "UN MISSION LIMIT",
                body: "Please select a customer first.",
            });
            return;
        }

        const missions = getModelRecords(pos, "un.mission");
        const missionLines = getModelRecords(pos, "un.mission.line");
        const categories = getModelRecords(pos, "rc.category");

        const mission = missions.find((m) => getId(m.id) === missionId);
        const period = mission?.un_mission_period || "month";

        let consumed = {};
        try {
            consumed = await pos.data.call(
                "pos.order",
                "get_un_mission_consumed_qty",
                [partnerId, missionId, period, false]
            );
        } catch (error) {
            console.error("Failed to check ration limit", error);
            this.dialog.add(AlertDialog, {
                title: "UN MISSION LIMIT",
                body: "Error while checking ration limits.",
            });
            return;
        }

        const qtyByCategory = {};
        for (const line of order.getOrderlines()) {
            const product = line.product_id || line.product;
            const catId = getId(product?.rc_category_id);
            if (!catId) continue;

            const qty = Number(line.qty || line.get_quantity?.() || 0);
            qtyByCategory[catId] = (qtyByCategory[catId] || 0) + qty;
        }

        for (const missionLine of missionLines) {
            if (getId(missionLine.mission_id) !== missionId) continue;

            const catId = getId(missionLine.category_id);
            const limit = Number(missionLine.limit || 0);
            const previous = Number(consumed[catId] || 0);
            const current = Number(qtyByCategory[catId] || 0);
            const total = previous + current;

            if (total > limit) {
                const category =
                    categories.find((c) => getId(c.id) === catId) || missionLine.category_id;

                this.dialog.add(AlertDialog, {
                    title: "UN MISSION LIMIT",
                    body: `YOU HAVE REACHED ${category?.name?.toUpperCase() || "CATEGORY"} LIMIT.`,
                    confirmLabel: "Ok",
                });
                return;
            }
        }

        return super.validateOrder(...arguments);
    },
});