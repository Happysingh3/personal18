from odoo import models, fields

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    auto_assign_user_id = fields.Many2one(
        'res.users',
        string='Responsible user (auto-assign)',
        help='User who will automatically be assigned to tasks in this stage.'
    )