# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class AeboDiscussHook(models.AbstractModel):
    _name = "aebo.discuss.hook"
    _description = "Hook to post birthday wishes to Discuss"

    @api.model
    def _get_birthday_channel(self):
        ICP = self.env["ir.config_parameter"].sudo()
        cid = ICP.get_param("birthday_knk.discuss_channel_id")
        if cid:
            chan = self.env["mail.channel"].sudo().browse(int(cid))
            if chan.exists():
                return chan
        # fallback: try a 'General' public channel
        chan = self.env["mail.channel"].sudo().search(
            [("name", "ilike", "General"), ("channel_type", "=", "channel")], limit=1
        )
        return chan

    @api.model
    def post_birthday_message(self, person_name, model=None, rec_id=None):
        channel = self._get_birthday_channel()
        if not channel:
            return False
        title = _("🎂 Happy Birthday %(name)s! 🎉", name=person_name or "")
        link = ""
        if model and rec_id:
            link = ("/web#id=%s&model=%s&view_type=form" % (rec_id, model)).replace(" ", "%20")
        if link:
            body = (
                f"<p><b>{title}</b></p>"
                f"<p>Join us in wishing <a href='{link}'>{person_name}</a> a wonderful birthday! 🎁</p>"
            )
        else:
            body = f"<p><b>{title}</b></p><p>Join us in sending warm wishes! 🎁</p>"
        channel.message_post(
        try:
            self.env['aebo.discuss.hook'].post_birthday_message(getattr(self, 'name', False) or getattr(self, 'display_name', False), self._name, self.id)
        except Exception:
            pass
            body=body,
            subject=_("Birthday Wishes: %s") % (person_name or ""),
            message_type="comment",
            subtype_xmlid="mail.mt_comment",
        )
        return True