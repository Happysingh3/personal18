from odoo import models,fields

class ResCompany(models.Model):
    _inherit = "res.company"

    global_search_model_ids = fields.Many2many("ir.model")