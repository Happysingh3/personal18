from odoo import fields, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    order_number = fields.Char(string="Order Number")
    client_details = fields.Char(string="Client Details")
    serial_number = fields.Char(string="Serial Number")
    crac_generated = fields.Char(string="CRAC Generated")

    # related flags (read-only) to expose project settings on task
    show_order_on_card_rel = fields.Boolean(
        string="Show Order on Kanban (Rel.)",
        related="project_id.show_order_on_card",
        readonly=True,
        store=False,
    )
    show_client_on_card_rel = fields.Boolean(
        string="Show Client on Kanban (Rel.)",
        related="project_id.show_client_on_card",
        readonly=True,
        store=False,
    )
    show_serial_on_card_rel = fields.Boolean(
        string="Show Serial on Kanban (Rel.)",
        related="project_id.show_serial_on_card",
        readonly=True,
        store=False,
    )
    show_crac_on_card_rel = fields.Boolean(
        string="CRAC Number on Kanban (Rel.)",
        related="project_id.show_crac_on_card",
        readonly=True,
        store=False,
    )