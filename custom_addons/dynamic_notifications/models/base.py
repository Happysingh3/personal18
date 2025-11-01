# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class BaseModelExtension(models.AbstractModel):
    _inherit = "base"

    @api.model_create_multi
    def create(self, vals_list):
        """Trigger notifications when a record is created."""
        records = super(BaseModelExtension, self).create(vals_list)
        model_name = self._name
        _logger.info(f"\n\nCreating records for model {model_name}")

        # Fetch all active notification configurations for this model
        notification_configs = self.env["notification.config"].sudo().search(
            [
                ("model_id.model", "=", model_name),
                ("active", "=", True),
                ("state", "=", "confirm"),
                ("on_create", "=", True),
            ],
        )

        if notification_configs:
            _logger.info(
                f"Found {len(notification_configs)} notification configs for model {model_name}"
            )

            for notification in notification_configs:
                for record in records:
                    name = getattr(record, "name", "Unnamed Record")
                    _logger.info(f"Sending notification for record: {name}")
                    notification._send_notification("created", name)

        return records

    def write(self, vals):
        """Trigger notifications when a monitored selection field changes."""
        _logger.info(f"Updating records in model {self._name}")

        # Fetch all notification configs for this model where state change is enabled
        notification_configs = self.env["notification.config"].sudo().search(
            [
                ("model_id.model", "=", self._name),
                ("active", "=", True),
                ("state", "=", "confirm"),
                ("on_state_change", "=", True),
                ("field_id", "!=", False),
            ]
        )

        if not notification_configs:
            return super().write(vals)

        result = super().write(vals)

        # Process notifications for state changes
        for notification in notification_configs:
            field_name = notification.field_id.name
            allowed_values = notification.selection.mapped("value")
            for record in self:
                new_value = record[field_name]
                if new_value in allowed_values:
                    name = getattr(record, "name", "Unnamed Record")
                    _logger.info(f"Sending notification for record: {name}")
                    notification._send_notification("updated", name)

        return result
