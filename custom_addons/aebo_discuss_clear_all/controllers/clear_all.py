# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class DiscussClearAll(http.Controller):

    @http.route("/aebo_discuss/clear_all", type="json", auth="user")
    def clear_all(self):
        env = request.env.sudo()
        partner = env.user.partner_id

        # Mark all unread notifications for this partner as read
        notifs = env["mail.notification"].search([
            ("res_partner_id", "=", partner.id),
            ("is_read", "=", False),
        ])
        if notifs:
            notifs.write({"is_read": True})

        # Advance last_seen for all channels to the last message (reset counters)
        mcp = env["mail.channel.partner"].search([("partner_id", "=", partner.id)])
        for rec in mcp:
            last_msg = rec.channel_id.last_message_id
            if last_msg and (not rec.last_seen_message_id or rec.last_seen_message_id.id < last_msg.id):
                rec.last_seen_message_id = last_msg.id

        return {"status": "ok"}