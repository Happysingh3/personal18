# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import AccessError

class MailChannel(models.Model):
    _inherit = "mail.channel"

    @api.model
    def _check_clear_chat_rights(self):
        if not self.env.user.has_group("aebo_discuss_clear_chat.group_discuss_clear_chat"):
            raise AccessError(_("You don't have rights to clear chats."))

    def action_clear_chat(self):
        """Delete all messages & attachments of this channel (DM or group)."""
        self._check_clear_chat_rights()
        for channel in self:
            msgs = self.env["mail.message"].sudo().search([
                ("model", "=", "mail.channel"),
                ("res_id", "=", channel.id),
            ])
            if not msgs:
                continue

            self.env["mail.notification"].sudo().search([
                ("mail_message_id", "in", msgs.ids)
            ]).unlink()

            atts = self.env["ir.attachment"].sudo().search([
                ("message_id", "in", msgs.ids)
            ])
            atts.unlink()

            msgs.unlink()
        return True
