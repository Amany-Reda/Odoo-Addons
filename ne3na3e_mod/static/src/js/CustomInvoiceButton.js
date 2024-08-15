odoo.define('your_module_name.CustomInvoiceButton', function (require) {
    'use strict';

    const InvoiceButton = require('point_of_sale.InvoiceButton');
    const Registries = require('point_of_sale.Registries');

    const CustomInvoiceButton = InvoiceButton => class extends InvoiceButton {
        async _downloadInvoice(orderId) {
            try {
                const [orderWithInvoice] = await this.rpc({
                    method: 'read',
                    model: 'pos.order',
                    args: [orderId, ['account_move']],
                    kwargs: { load: false },
                });
                if (orderWithInvoice && orderWithInvoice.account_move) {
                    await this.env.legacyActionManager.do_action(this.env.pos.newInvoiceReportAction, {
                        additional_context: {
                            active_ids: [orderWithInvoice.account_move],
                        },
                    });
                }
            } catch (error) {
                if (error instanceof Error) {
                    throw error;
                } else {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Network Error'),
                        body: this.env._t('Unable to download invoice.'),
                    });
                }
            }
        }
    };

    // Register the extended component
    Registries.Component.extend(InvoiceButton, CustomInvoiceButton);

    return InvoiceButton;
});
