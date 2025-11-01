from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = "project.project"

    # Settings to control what shows on task kanban cards
    show_order_on_card = fields.Boolean(string="Show Order # on Kanban", default=True)
    show_client_on_card = fields.Boolean(string="Show Client on Kanban", default=True)
    show_serial_on_card = fields.Boolean(string="Show Serial # on Kanban", default=True)
    show_crac_on_card = fields.Boolean(string="Show CRAC # on Kanban", default=True)