from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    recycle_bin_lifecycle = fields.Integer(
        string='Clear Recycle Bin Lifecycle',
        help='Number of days after which recycle bin records will be automatically deleted.',
        config_parameter='recycle_bin.lifecycle_days',  
        default=30  # Default lifecycle days
    )
