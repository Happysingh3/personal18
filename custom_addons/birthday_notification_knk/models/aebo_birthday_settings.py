# -*- coding: utf-8 -*-
from odoo import api, fields, models

class AeboBirthdayDiscussSettings(models.TransientModel):
    _name = "aebo.birthday.discuss.settings"
    _description = "Birthday Discuss Settings"

    discuss_channel_id = fields.Many2one("mail.channel", string="Birthday Wishes Channel")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        ICP = self.env["ir.config_parameter"].sudo()
        cid = int(ICP.get_param("birthday_knk.discuss_channel_id", "0") or 0)
        res["discuss_channel_id"] = cid or False
        return res

    def action_save(self):
        self.ensure_one()
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.set_param("birthday_knk.discuss_channel_id", self.discuss_channel_id.id or 0)
        return {"type": "ir.actions.act_window_close"}
