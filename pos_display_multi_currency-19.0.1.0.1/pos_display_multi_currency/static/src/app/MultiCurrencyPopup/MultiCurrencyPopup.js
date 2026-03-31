/** @odoo-module */
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
import { _t } from "@web/core/l10n/translation";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { Input } from "@point_of_sale/app/components/inputs/input/input";
import { Dialog } from "@web/core/dialog/dialog";
import { patch } from "@web/core/utils/patch";
import { useAsyncLockedMethod } from "@point_of_sale/app/hooks/hooks";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";

export class WkDisplaycCurrmultiPopup extends Component {
    static template = "pos_display_multi_currency.WkDisplaycCurrmultiPopup";
    static components = { Input, Dialog };
    static defaultProps = {
        title: 'Confirm ?'
        , value: ''
    }
    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.orm = useService("orm");
        super.setup();
    }
    get selected_currency() {
        return this.props.selected_currency
    }
    wk_change_currency(e) {
        var self = this;
        var sel_curr_data;
        var sel_curr_id = $('#wk_currencies').children(":selected").attr("id");
        if (sel_curr_id)
            sel_curr_data = self.env.services.pos.wk_display_curr_ids.filter(curr => curr.id == sel_curr_id);
        if (sel_curr_data && sel_curr_data[0] && sel_curr_data.length == 1) {
            self.pos.secondary_currency = sel_curr_data[0];
            var order = self.pos.getOrder();
            self.props.selected_currency = sel_curr_data[0];
            const res = this.orm.call(
                'pos.config',
                'set_selected_currency',
                [1, self.pos.secondary_currency.id, self.pos.config.id],
            )
            if (res) {
                self.props.close();
                self.env.services.pos.navigate("PaymentScreen", {
                    orderUuid: self.env.services.pos.selectedOrderUuid,
                });
                setTimeout(function () {
                    self.env.services.pos.navigate("ProductScreen");
                }, 1);
            }
        }
    }
};
patch(ControlButtons.prototype, {
    setup() {
        super.setup(...arguments);
        this.multi_currency = useAsyncLockedMethod(this.multi_currency);
    },
    async multi_currency() {
        var self = this;
        self.dialog.add(WkDisplaycCurrmultiPopup,
            { selected_currency: self.pos.secondary_currency })
    },
    get currentCurrencyName() {
        return this.pos.secondary_currency ? this.pos.secondary_currency.name : _t('Multi Currencies');
    }
});
