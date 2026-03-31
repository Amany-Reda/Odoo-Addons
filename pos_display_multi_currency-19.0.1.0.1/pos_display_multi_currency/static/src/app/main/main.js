/** @odoo-module */
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { PaymentScreenStatus } from "@point_of_sale/app/screens/payment_screen/payment_status/payment_status";
import { PaymentScreenPaymentLines } from "@point_of_sale/app/screens/payment_screen/payment_lines/payment_lines";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { formatMonetary } from "@web/views/fields/formatters";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import {
    formatFloat,
    roundDecimals,
    floatIsZero as genericFloatIsZero,
} from "@web/core/utils/numbers";
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";

patch(OrderReceipt.prototype,{
    formatCurrency(amount, hasSymbol = true) {
        const mainCurrency = super.formatCurrency(amount, hasSymbol);
        if (this.env.services.pos && this.env.services.pos.config.enable_display_multi_curr) {
            const secondaryCurrency = this.env.services.pos.wk_format_currency(amount, hasSymbol);
            return `${mainCurrency} / ${secondaryCurrency}`;
        }
        return mainCurrency;
    }
});

patch(ReceiptScreen.prototype, {
    get orderAmountPlusTip() {
        var orderAmountStr = super.orderAmountPlusTip
        if (!this.env.services.pos.config.enable_display_multi_curr){
            return orderAmountStr
        }
        const order = this.currentOrder;
        const orderTotalAmount = order.priceIncl;
        const tip_product_id = this.pos.config.tip_product_id?.[0];
        const tipLine = order
            .getOrderlines()
            .find((line) => tip_product_id && line.product.id === tip_product_id);
        const tipAmount = tipLine ? tipLine.get_all_prices().priceWithTax : 0;
        
        const wkorderAmountStr = this.env.services.pos.wk_format_currency(orderTotalAmount - tipAmount);
        if (!tipAmount) {
            return `${orderAmountStr} / ${wkorderAmountStr}`;
        }
        const wktipAmountStr = this.env.services.pos.wk_format_currency(tipAmount);
        orderAmountStr = this.env.utils.formatCurrency(orderTotalAmount - tipAmount);
        const tipAmountStr = this.env.utils.formatCurrency(tipAmount);
        return `${orderAmountStr} / ${wkorderAmountStr} + ${tipAmountStr} / ${wktipAmountStr} tip`;
    },
});


patch(PaymentScreenStatus.prototype, {
    get wkchangeText() {
        return this.env.services.pos.wk_format_currency(this.props.order.change);
    },
    get wkremainingText() {
        return this.env.services.pos.wk_format_currency(
            this.props.order.remainingDue > 0 ? this.props.order.remainingDue : 0
        );
    }
});

patch(PaymentScreenPaymentLines.prototype, {
    formatLineAmount(paymentline) {
        return this.env.utils.formatCurrency(paymentline.getAmount());
    },
    wkformatLineAmount(paymentline) {
        return this.env.services.pos.wk_format_currency(paymentline.getAmount());
    }
});

patch(ProductCard.prototype, {
    get getWkFormattedUnitPrice() {
        let product_price = this.props.product.list_price
        // let price = product_price.replace(/[^0-9.]/g, '');
        const formattedUnitPrice = this.env.services.pos.wk_format_currency(product_price);
        return formattedUnitPrice
    }
});

patch(PosStore.prototype, {
    wk_format_currency(amount ,hasSymbol = true) {
        if (!this.config.enable_display_multi_curr){
            return ""
        }
        amount = this.wk_roundCurrency(amount*this.secondary_currency.rate)
        const res = formatMonetary(amount, {
            currencyId: this.secondary_currency.id,
            noSymbol: !hasSymbol,
        })
        return res;
    },    
    wk_roundCurrency(value) {
        return roundDecimals(value, this.secondary_currency.decimal_places)
    },
    wk_floatIsZero (value) {
        return genericFloatIsZero(value, this.secondary_currency.decimal_places);
    },
    async processServerData() {
        await super.processServerData(...arguments);
        var self = this;
        self.wk_display_curr_ids = await this.env.services.orm.silent.call(
             'pos.session',
             'pos_ui_multi_currencies_data_load',
             [[odoo.pos_session_id]],
        );
        self.secondary_currency =this.currency
        if (self.config.enable_display_multi_curr && self.config.wk_sel_int_currency){
            var currency= self.wk_display_curr_ids.filter((curr) => curr.id === self.config.wk_sel_int_currency)[0]
            if (currency){
                self.secondary_currency=currency
            }
        }else if (self.config.enable_display_multi_curr && self.config.wk_default_currency_id){
            var currency= self.wk_display_curr_ids.filter((curr) => curr.id === self.config.wk_default_currency_id[0])[0]
            if (currency){
                self.secondary_currency=currency
            }
        }          
    }
});
