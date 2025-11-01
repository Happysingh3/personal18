# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InheritCRMKanbanView(models.Model):
    _inherit = 'crm.lead'
    _description = 'Inherit CRM Lead'


    def action_open_form_view(self):
        self.ensure_one()  # Ensure only one record is processed
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

