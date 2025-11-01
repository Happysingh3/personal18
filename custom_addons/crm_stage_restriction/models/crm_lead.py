from odoo import models, api, _
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_payment_stage_id(self):
        stage = self.env['crm.stage'].search([('name', '=', 'Payment Received')], limit=1)
        return stage.id if stage else False

    def write(self, vals):
        payment_stage_id = self.get_payment_stage_id()
        if 'stage_id' in vals and payment_stage_id:
            for lead in self:
                if vals['stage_id'] == payment_stage_id:
                    allowed_user_ids = [self.env.ref('base.user_admin').id, 11]  # Change this to your actual user ID or XML ID
                    if self.env.uid not in allowed_user_ids:
                        raise UserError(_("You are not allowed to move lead to 'Payment Received' stage."))
        return super(CrmLead, self).write(vals)
