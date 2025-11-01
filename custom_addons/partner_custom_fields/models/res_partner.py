from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    unit_name = fields.Char(string="Unit Name")
    unit_location = fields.Char(string="Unit Location")
    tender_id = fields.Char(string="Tender ID")
    lead_source = fields.Char(string="Lead Source")
    prebid_date = fields.Date(string="Prebid Date")
    prebid_location = fields.Char(string="Prebid Location")
    

    @api.constrains('phone')
    def _check_unique_phone(self):
        for rec in self:
            if rec.phone:
                existing = self.env['res.partner'].sudo().search([
                    ('phone', '=', rec.phone),
                    ('id', '!=', rec.id)
                ], limit=1)
                if existing:
                    raise ValidationError("🚫 This mobile number already exists in the system.")