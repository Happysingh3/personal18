from odoo import models,fields

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    global_search_model_ids = fields.Many2many("ir.model",related="company_id.global_search_model_ids",readonly=False)