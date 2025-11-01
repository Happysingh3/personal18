# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class MessagingMenuMarkAll(http.Controller):

    @http.route("/aebo_messaging_menu/clear_all", type="json", auth="user")
    def clear_all(self):
        env = request.env
        partner = env.user.partner_id

        # A) Discuss Inbox (needaction) -> built-in helper
        try:
            env['mail.message'].mark_all_as_read()
        except Exception:
            pass

        # B) Notifications -> read
        notif_domain = [('res_partner_id', '=', partner.id), ('is_read', '=', False)]
        notif_before = env['mail.notification'].search_count(notif_domain)
        notifs = env['mail.notification'].search(notif_domain, limit=100000)
        if notifs:
            notifs.sudo().write({'is_read': True})
        notif_after = env['mail.notification'].search_count(notif_domain)

        # C) Email-failure style entries (cover multiple builds)
        failures_cleared = 0

        # C1) Preferred: mail.failure (newer builds)
        try:
            Failure = env['mail.failure'].sudo()  # sudo to avoid ACL on read
            fields = Failure._fields

            # collect by partner (try both field names, OR logic by union)
            failures = Failure.browse()
            if 'res_partner_id' in fields:
                failures |= Failure.search([('res_partner_id', '=', partner.id)], limit=100000)
            if 'partner_id' in fields:
                failures |= Failure.search([('partner_id', '=', partner.id)], limit=100000)

            if failures:
                # keep only unread/unhandled if those flags exist
                to_write = failures
                if 'is_read' in fields:
                    to_write = to_write.filtered(lambda r: not getattr(r, 'is_read', False))
                if 'is_handled' in fields:
                    to_write = to_write.filtered(lambda r: not getattr(r, 'is_handled', False))

                vals = {}
                if 'is_read' in fields:
                    vals['is_read'] = True
                if 'is_handled' in fields:
                    vals['is_handled'] = True

                if vals and to_write:
                    to_write.write(vals)
                    failures_cleared += len(to_write)
        except KeyError:
            # mail.failure not present -> ignore
            pass

        # C2) Fallback: legacy exceptions on mail.mail (ACL-safe via sudo)
        try:
            Mail = env['mail.mail'].sudo()  # sudo also for search
            if 'state' in Mail._fields:
                excs = Mail.search([('state', '=', 'exception')], limit=100000)
                if excs:
                    vals = {}
                    for opt in ('is_read', 'is_handled', 'handled'):
                        if opt in Mail._fields:
                            vals[opt] = True
                    if vals:
                        excs.write(vals)
                        failures_cleared += len(excs)
        except KeyError:
            pass

        # D) Channel counters -> last_seen to last_message (both member models)
        def bump_members(model_name):
            try:
                Member = env[model_name]
            except KeyError:
                return 0
            touched = 0
            members = Member.search([('partner_id', '=', partner.id)], limit=100000)
            for m in members:
                ch = getattr(m, 'channel_id', False) or getattr(m, 'channel', False)
                if not ch:
                    continue
                last = getattr(ch, 'last_message_id', False)
                if not last and hasattr(ch, 'message_ids'):
                    msgs = ch.message_ids
                    last = msgs and msgs[-1]
                if not last:
                    continue

                vals = {}
                for fld in ('last_seen_message_id', 'last_seen_msg_id', 'last_seen'):
                    if hasattr(m, fld):
                        vals[fld] = last.id
                        break
                if vals:
                    m.sudo().write(vals)
                    touched += 1
            return touched

        channels_touched = bump_members('discuss.channel.member')
        if not channels_touched:
            channels_touched = bump_members('mail.channel.partner')

        return {
            'status': 'ok',
            'notifications': {'before': notif_before, 'after': notif_after},
            'channels_touched': channels_touched,
            'failures_cleared': failures_cleared,
        }