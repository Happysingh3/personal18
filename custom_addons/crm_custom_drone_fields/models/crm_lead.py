from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    product_selection = fields.Selection([
        ('rakshak_45', 'Aebo Rakshak 45'),
        ('establishment_lab', 'Drone Establishment Lab'),
        ('custom_drone', 'Custom Drone'),
    ], string='Product')

    drone_detail = fields.Char(string='Drone Details')
