from odoo import api, fields, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    template_task_id = fields.Many2one(
        "project.task",
        string="Template Task",
        help="Pick an existing task; its subtasks will be copied here.",
        domain="[('project_id', '=', project_id), ('child_ids', '!=', False)]",
    )

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super().create(vals_list)
        for task, vals in zip(tasks, vals_list):
            template_id = vals.get("template_task_id") or task.template_task_id.id
            if not template_id:
                continue
            template_children = self.search([("parent_id", "=", template_id)])
            for child in template_children:
                self.create({
                    "name": child.name,
                    "parent_id": task.id,
                    "project_id": task.project_id.id,
                    "description": child.description or False,
                    "user_ids": [(6, 0, child.user_ids.ids)],
                    "stage_id": task.stage_id.id,
                })
        return tasks