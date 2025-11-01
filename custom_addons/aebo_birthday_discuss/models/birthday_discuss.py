# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class AeboBirthdaySettings(models.TransientModel):
    _name = "aebo.birthday.settings"
    _description = "Birthday Wishes Settings"

    birthday_channel_id = fields.Many2one(
        "mail.channel",
        string="Birthday Wishes Channel",
        help="Discuss channel where automatic birthday wishes will be posted."
    )
    birthday_include_contacts = fields.Boolean(
        string="Include Contacts (not only Employees)",
        default=True,
        help="Also wish birthdays for partners (Contacts) with a birth date."
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        ICP = self.env["ir.config_parameter"].sudo()
        cid = int(ICP.get_param("aebo_birthday_discuss.channel_id", "0") or 0)
        res["birthday_channel_id"] = cid or False
        res["birthday_include_contacts"] = ICP.get_param("aebo_birthday_discuss.include_contacts", "1") == "1"
        return res

    def action_save(self):
        self.ensure_one()
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.set_param("aebo_birthday_discuss.channel_id", self.birthday_channel_id.id or 0)
        ICP.set_param("aebo_birthday_discuss.include_contacts", "1" if self.birthday_include_contacts else "0")
        return {"type": "ir.actions.act_window_close"}


class AeboBirthdayDiscuss(models.AbstractModel):
    _name = "aebo.birthday.discuss"
    _description = "Post birthday wishes to Discuss channel"

    @api.model
    def _today(self):
        return fields.Date.context_today(self.env.user)

    @api.model
    def _get_channel(self):
        ICP = self.env["ir.config_parameter"].sudo()
        cid = ICP.get_param("aebo_birthday_discuss.channel_id")
        channel = cid and self.env["mail.channel"].sudo().browse(int(cid)) or False
        if not channel or not channel.exists():
            channel = self.env["mail.channel"].sudo().search(
                [("name", "ilike", "General"), ("channel_type", "=", "channel")],
                limit=1
            )
        return channel

    @api.model
    def _format_body(self, name, model=None, rec_id=None):
        link = ""
        if model and rec_id:
            link = ("/web#id=%s&model=%s&view_type=form" % (rec_id, model)).replace(" ", "%20")
        title = _("🎂 Happy Birthday %(name)s! 🎉", name=name)
        if link:
            body = (
                f"<p><b>{title}</b></p>"
                f"<p>Join us in wishing <a href='{link}'>{name}</a> a wonderful birthday! 🎁</p>"
            )
        else:
            body = f"<p><b>{title}</b></p><p>Join us in sending warm wishes! 🎁</p>"
        return body

    @api.model
    def cron_post_birthday_messages(self):
        today = self._today()
        channel = self._get_channel()
        if not channel:
            return
        posted_any = False

        employees = self.env["hr.employee"].sudo().search([("birthday", "!=", False)])
        for emp in employees:
            try:
                if emp.birthday and emp.birthday.month == today.month and emp.birthday.day == today.day:
                    body = self._format_body(emp.name, "hr.employee", emp.id)
                    channel.message_post(
                        body=body,
                        subject=_("Birthday Wishes: %s") % emp.name,
                        message_type="comment",
                        subtype_xmlid="mail.mt_comment",
                    )
                    posted_any = True
            except Exception:
                continue

        ICP = self.env["ir.config_parameter"].sudo()
        include_contacts = ICP.get_param("aebo_birthday_discuss.include_contacts", "1") == "1"

        if include_contacts and "birthdate_date" in self.env["res.partner"]._fields:
            partners = self.env["res.partner"].sudo().search([("birthdate_date", "!=", False)])
            for p in partners:
                try:
                    if p.birthdate_date and p.birthdate_date.month == today.month and p.birthdate_date.day == today.day:
                        if getattr(p, "employee_ids", False):
                            continue
                        body = self._format_body(p.name, "res.partner", p.id)
                        channel.message_post(
                            body=body,
                            subject=_("Birthday Wishes: %s") % p.name,
                            message_type="comment",
                            subtype_xmlid="mail.mt_comment",
                        )
                        posted_any = True
                except Exception:
                    continue

        return posted_any
