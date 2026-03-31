/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

function getId(value) {
    if (!value) {
        return false;
    }
    if (Array.isArray(value)) {
        return value[0];
    }
    if (typeof value === "object" && "id" in value) {
        return value.id;
    }
    return value;
}

function getModelRecords(store, modelName) {
    const model = store.models?.[modelName];
    if (!model) {
        return [];
    }
    if (typeof model.getAll === "function") {
        return model.getAll();
    }
    if (model.records) {
        return Object.values(model.records);
    }
    return [];
}

function buildCurrentQtyByCategory(order) {
    const qtyByCategory = {};
    const orderlines = order?.getOrderlines ? order.getOrderlines() : [];

    for (const line of orderlines) {
        const product = line.product_id || null;
        const categoryId = getId(product?.rc_category_id);
        if (!categoryId) {
            continue;
        }
        const qty = Number(line.qty || 0);
        qtyByCategory[categoryId] = (qtyByCategory[categoryId] || 0) + qty;
    }

    return qtyByCategory;
}

async function getConsumedByCategory(pos, order, missionId) {
    const partner = order?.getPartner?.();
    const partnerId = partner?.id;
    if (!partnerId || !missionId) {
        return {};
    }

    const missions = getModelRecords(pos, "un.mission");
    const mission = missions.find((m) => getId(m.id) === missionId);
    const period = mission?.un_mission_period || "month";

    let excludeOrderId = false;
    if (typeof order.id === "number") {
        excludeOrderId = order.id;
    }

    return await pos.data.call(
        "pos.order",
        "get_un_mission_consumed_qty",
        [partnerId, missionId, period, excludeOrderId]
    );
}

function buildMissionReceiptData(pos, order, previousQtyByCategory = {}) {
    const config = pos?.config;
    const missionId = getId(config?.un_mission_id);
    if (!config?.enable_ration || !missionId || !order) {
        return false;
    }

    const missions = getModelRecords(pos, "un.mission");
    const missionLines = getModelRecords(pos, "un.mission.line");
    const categories = getModelRecords(pos, "rc.category");
    const mission = missions.find((m) => getId(m.id) === missionId);

    const currentQtyByCategory = buildCurrentQtyByCategory(order);

    const lines = missionLines
        .filter((line) => getId(line.mission_id) === missionId)
        .map((line) => {
            const categoryId = getId(line.category_id);
            const category =
                categories.find((c) => getId(c.id) === categoryId) || line.category_id;

            const previousQty = Number(previousQtyByCategory[categoryId] || 0);
            const currentQty = Number(currentQtyByCategory[categoryId] || 0);
            const totalQty = previousQty + currentQty;
            const limit = Number(line.limit || 0);

            return {
                category_id: categoryId,
                category_name: category?.name || "",
                previous_qty: previousQty,
                current_qty: currentQty,
                qty: totalQty,
                limit: limit,
                display_value: `${totalQty} / ${limit}`,
            };
        });

    return {
        id: missionId,
        name: mission?.name || "",
        period: mission?.un_mission_period || "",
        lines,
    };
}

async function checkRationLimit(pos, order, extraCategoryId = false, extraQty = 0) {
    const config = pos?.config;
    const missionId = getId(config?.un_mission_id);

    if (!config?.enable_ration || !missionId || !order) {
        return { ok: true };
    }

    const partner = order.getPartner?.();
    if (!partner?.id) {
        return {
            ok: false,
            title: "UN MISSION LIMIT",
            body: "PLEASE SELECT CUSTOMER FIRST.",
        };
    }

    const previousQtyByCategory = await getConsumedByCategory(pos, order, missionId);
    const currentQtyByCategory = buildCurrentQtyByCategory(order);

    if (extraCategoryId) {
        currentQtyByCategory[extraCategoryId] =
            (currentQtyByCategory[extraCategoryId] || 0) + Number(extraQty || 0);
    }

    const missionLines = getModelRecords(pos, "un.mission.line");
    const categories = getModelRecords(pos, "rc.category");

    for (const missionLine of missionLines) {
        if (getId(missionLine.mission_id) !== missionId) {
            continue;
        }

        const categoryId = getId(missionLine.category_id);
        const previousQty = Number(previousQtyByCategory[categoryId] || 0);
        const currentQty = Number(currentQtyByCategory[categoryId] || 0);
        const totalQty = previousQty + currentQty;
        const limit = Number(missionLine.limit || 0);

        if (totalQty > limit) {
            const category =
                categories.find((c) => getId(c.id) === categoryId) || missionLine.category_id;
            return {
                ok: false,
                title: "UN MISSION LIMIT",
                body: `YOU HAVE REACHED ${category?.name?.toUpperCase() || "CATEGORY"} LIMIT.`,
            };
        }
    }

    return { ok: true };
}

patch(PosStore.prototype, {
    async printReceipt({ basic = false, order = this.getOrder(), printBillActionTriggered = false } = {}) {
        console.warn("RATION printReceipt CALLED", order);

        if (order) {
            try {
                const missionId = getId(this.config?.un_mission_id);
                let previousQtyByCategory = {};
                if (this.config?.enable_ration && missionId) {
                    previousQtyByCategory = await getConsumedByCategory(this, order, missionId);
                }
                order._un_mission_receipt_data = buildMissionReceiptData(
                    this,
                    order,
                    previousQtyByCategory
                );
                console.warn("RATION receipt data", order._un_mission_receipt_data);
            } catch (error) {
                console.error("Failed to prepare ration receipt data", error);
                order._un_mission_receipt_data = false;
            }
        }

        return await super.printReceipt(...arguments);
    },

    async addLineToOrder(vals, order, opts = {}, configure = true) {
        const config = this.config;
        const missionId = getId(config?.un_mission_id);

        if (config?.enable_ration && missionId && order) {
            let product = vals.product_id || null;

            if (!product && vals.product_tmpl_id?.product_variant_ids?.length) {
                product = vals.product_tmpl_id.product_variant_ids[0];
            }

            const categoryId = getId(product?.rc_category_id);
            const qtyToAdd = Number(vals.qty || 1);

            if (categoryId) {
                try {
                    const check = await checkRationLimit(this, order, categoryId, qtyToAdd);
                    if (!check.ok) {
                        this.dialog.add(AlertDialog, {
                            title: check.title,
                            body: check.body,
                            confirmLabel: "Ok",
                        });
                        return;
                    }
                } catch (error) {
                    console.error("Failed to check ration limit on add product", error);
                    this.dialog.add(AlertDialog, {
                        title: "UN MISSION LIMIT",
                        body: "ERROR WHILE CHECKING RATION LIMITS.",
                        confirmLabel: "Ok",
                    });
                    return;
                }
            }
        }

        return await super.addLineToOrder(...arguments);
    },
});

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        const order = this.currentOrder;

        try {
            const check = await checkRationLimit(this.pos, order, false, 0);
            if (!check.ok) {
                this.dialog.add(AlertDialog, {
                    title: check.title,
                    body: check.body,
                    confirmLabel: "Ok",
                });
                return;
            }
        } catch (error) {
            console.error("Failed to check ration limit on payment", error);
            this.dialog.add(AlertDialog, {
                title: "UN MISSION LIMIT",
                body: "ERROR WHILE CHECKING RATION LIMITS.",
                confirmLabel: "Ok",
            });
            return;
        }

        return await super.validateOrder(...arguments);
    },
});