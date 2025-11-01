# models/discuss_channel.py
# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.exceptions import AccessError

class DiscussChannel(models.Model):
    _inherit = "discuss.channel"  # Odoo 18

    def _check_member_or_raise(self):
        uid_partner = self.env.user.partner_id
        for ch in self:
            if uid_partner not in ch.channel_partner_ids:
                raise AccessError(_("You are not a member of this chat."))
        return True

    def action_aebo_purge(self):
        """
        Permanently delete a chat for everyone:
        - messages: mail.message where (model in {'discuss.channel','mail.channel'} AND res_id = channel.id)
        - attachments on those messages OR directly on the channel
        - mail.notification (and mail.failure if present) for those messages
        - finally delete the channel
        """
        self = self.sudo()
        self._check_member_or_raise()

        Attachment   = self.env["ir.attachment"].sudo()
        Message      = self.env["mail.message"].sudo()
        Notification = self.env["mail.notification"].sudo()
        Failure      = self.env["mail.failure"].sudo() if "mail.failure" in self.env else None

        for ch in self:
            # messages linked to this channel via model/res_id (cover both old/new)
            msgs = Message.search([
                ('res_id', '=', ch.id),
                ('model', 'in', ['discuss.channel', 'mail.channel']),
            ])
            msg_ids = msgs.ids

            # attachments on those messages OR directly on the channel
            atts = Attachment.search([
                '|',
                    '&', ('res_model', '=', 'mail.message'),    ('res_id', 'in', msg_ids),
                    '&', ('res_model', '=', 'discuss.channel'), ('res_id', 'in', [ch.id]),
            ])
            if atts:
                atts.unlink()

            if msg_ids:
                notifs = Notification.search([('mail_message_id', 'in', msg_ids)])
                if notifs:
                    notifs.unlink()
                if Failure:
                    fails = Failure.search([('message_id', 'in', msg_ids)])
                    if fails:
                        fails.unlink()
                msgs.unlink()

            # finally delete the channel itself
            ch.unlink()

        return True