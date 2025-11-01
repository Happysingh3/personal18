// Odoo 18 (OWL) - Add "Clear chat" action in Discuss thread menu
odoo.define('aebo_discuss_clear_chat.clear_chat', async (require) => {
    "use strict";
    const { registry } = require("@web/core/registry");
    const { _t } = require("@web/core/l10n/translation");
    const rpc = require('web.rpc');

    const threadActionsRegistry = registry.category("mail.thread_actions");

    threadActionsRegistry.add("aebo_clear_chat", {
        isVisible(env, thread) {
            return thread && thread.model === "mail.channel";
        },
        sequence: 999,
        icon: "fa fa-trash",
        label: _t("Clear chat"),
        async onClick(env, thread) {
            const Dialog = (await require("@web/core/confirmation_dialog/confirmation_dialog")).ConfirmationDialog;
            const { openDialog } = require("@web/core/dialog/dialog_service");
            openDialog(Dialog, {
                title: _t("Delete all messages?"),
                body: _t("This will permanently delete all messages and attachments in this chat for all members."),
                confirmLabel: _t("Delete"),
                confirmClass: "btn-danger",
                async confirm() {
                    await rpc.query({
                        model: "mail.channel",
                        method: "action_clear_chat",
                        args: [[thread.id]],
                    });
                    window.location.reload();
                },
            });
        },
    });
});
