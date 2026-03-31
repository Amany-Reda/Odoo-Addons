/** @odoo-module */
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

import { OrderDisplay } from "@point_of_sale/app/components/order_display/order_display";
import { patch } from "@web/core/utils/patch";

patch(OrderDisplay, {
    props: {
        ...OrderDisplay.props,
        Wk_tatal: { String ,optional: true},
        Wk_tax: { String ,optional: true },
    },
});
