from odoo import api, models

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model_create_multi
    def create(self, vals_list, **kwargs):
        # always pass **kwargs through to super()
        tasks = super().create(vals_list, **kwargs)
        for task in tasks:
            task._apply_stage_auto_assign()
        return tasks

    def write(self, vals, **kwargs):
        res = super().write(vals, **kwargs)
        if 'stage_id' in vals:
            for task in self:
                task._apply_stage_auto_assign()
        return res

    def _apply_stage_auto_assign(self):
        """Assign exactly one user from the stage (if configured)."""
        if self.stage_id and self.stage_id.auto_assign_user_id:
            self.user_ids = [(6, 0, [self.stage_id.auto_assign_user_id.id])]
        return True