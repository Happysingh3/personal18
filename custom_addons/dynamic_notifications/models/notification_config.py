# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NotificationConfig(models.Model):
    _name = "notification.config"
    _description = "Notification Configuration"

    name = fields.Char(string="Name", required=True)
    on_create = fields.Boolean(string="On Create", default=True)
    on_state_change = fields.Boolean(string="On State Change")
    active = fields.Boolean(
        "Active",
        default=True,
    )

    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        required=True,
        ondelete="cascade",
    )
    notification_user_ids = fields.Many2many("res.users", string="Notify User")

    field_id = fields.Many2one(
        "ir.model.fields",
        string="Field",
        domain="[('model_id', '=', model_id), ('ttype', '=', 'selection')]",
        ondelete="cascade",
    )

    selection = fields.Many2many(
        "ir.model.fields.selection",
        string="State",
        domain="[('field_id', '=', field_id)]",
        help="Select state values that should trigger notifications.",
    )

    notification_type = fields.Selection(
        [("info", "Info"), ("warning", "Warning"), ("danger", "Danger")],
        string="Notification Type",
    )
    state = fields.Selection(
        [("draft", "Draft"), ("confirm", "Confirmed")], string="State", default="draft"
    )

    def action_confirm(self):
        self.state = "confirm"

    def action_reset_to_draft(self):
        self.state = "draft"

    def _send_notification(self, action, record_name):
        creator = self.create_uid.name if self.create_uid else "System"
        for user in self.notification_user_ids:
            # Send real-time notification
            # self.env["bus.bus"].sendone(
            #     (self._name, user.id),
            #     {"message": f"Record {self.name} in {self.model_id.model} has been {action} by {creator}", "type": action},
            # )

            # Send email notification
            template = self.env.ref("mail.mail_notification_light")
            if template:
                mail_values = {
                    "subject": f"Record {record_name} in {self.model_id.model} {action}",
                    "body_html": f"""
                        <p>Hello {user.name},</p>
                        <p>The record <b>{record_name}</b> in <b>{self.model_id.model}</b> has been <b>{action}</b>.</p>
                        <p>This action was performed by <b>{creator}</b>.</p>
                        <p>Best Regards,<br/>Your Odoo System</p>
                    """,
                    "email_to": user.email,
                }
                self.env["mail.mail"].sudo().create(mail_values).send()