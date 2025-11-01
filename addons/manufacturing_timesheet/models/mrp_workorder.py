# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Technologies(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
from datetime import datetime
from odoo import fields, models, api


class MrpWorkorder(models.Model):
    """Inherited model mrp_workorder to add field and functions related to
       manufacturing timesheet.

        Methods:
            button_start(self):
                Supering the function of start button to start the time of
                timesheet.
            button_pending(self):
                Supering the function of pause button to set timesheet in
                progress state.
            button_finish(self):
                Supering the function of done button to calculate total
                time in timesheet.
    """
    _inherit = 'mrp.workorder'

    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  readonly=False, required=True,
                                  help='Employee in work order', compute="_compute_employee_id",store=True)

    def button_start(self):
        """ Supering the function of start button to start the timer
            of timesheet.

            Boolean: Returns true
        """
        res = super(MrpWorkorder, self).button_start()
        project = self.env['project.project'].search(
            [('name', '=', ("MO: {}".format(self.production_id.name)))])
        if project:
            task_id = project.task_ids.search([('name', '=', (
                "{} in {} for {} on {}".format(self.name,
                                               self.workcenter_id.name,
                                               self.product_id.display_name,
                                               str(self.date_start))))])
            if not task_id:
                task_id = self.env['project.task'].create({
                    'name': ("{} in {} for {} on {}".format(self.name,
                                                            self.workcenter_id.name,
                                                            self.product_id.display_name,
                                                            str(self.date_start))),
                    'project_id': project.id,
                    'date_assign': self.date_start,
                    'date_deadline': self.date_finished,
                    'allocated_hours': self.duration_expected,
                })
                self.env['account.analytic.line'].create({
                    'task_id': task_id.id,
                    'date': datetime.today(),
                    'name': ("{} in {} for {}".format(self.name,
                                                      self.workcenter_id.name,
                                                      self.product_id.display_name)),
                    'employee_id': self.employee_id.id,
                    'is_manufacturing': True
                })
        else:
            project_id = self.env['project.project'].create(
                {'name': ("MO: {}".format(self.production_id.name)),
                 'is_manufacturing': True})
            task_id = project_id.task_ids.search([('name', '=', (
                "{} in {} for {} on {}".format(self.name,
                                               self.workcenter_id.name,
                                               self.product_id.display_name,
                                               str(self.date_start))))])
            if not task_id:
                task_id = self.env['project.task'].create({
                    'name': ("{} in {} for {} on {}".format(self.name,
                                                            self.workcenter_id.name,
                                                            self.product_id.display_name,
                                                            str(self.date_start))),
                    'project_id': project_id.id,
                    'date_assign': self.date_start,
                    'date_deadline': self.date_finished,
                    'allocated_hours': self.duration_expected,
                })
                self.env['account.analytic.line'].create({
                    'task_id': task_id.id,
                    'date': datetime.today(),
                    'name': ("{} in {} for {}".format(self.name,
                                                      self.workcenter_id.name,
                                                      self.product_id.display_name)),
                    'employee_id': self.employee_id.id,
                    'is_manufacturing': True
                })
        return res

    def button_pending(self):
        """ Supering the function of pause button to set timesheet in
            progress state.

            Boolean: Returns true
        """
        res = super(MrpWorkorder, self).button_pending()
        project = self.env['project.project'].search(
            [('name', '=', ("MO: {}".format(self.production_id.name)))])
        task_id = project.task_ids.search([('name', '=', (
            "{} in {} for {} on {}".format(self.name, self.workcenter_id.name,
                                           self.product_id.display_name,
                                           str(self.date_start))))])
        task_id.write({
            'allocated_hours': self.duration_expected
        })
        timesheet = task_id.mapped('timesheet_ids')
        for rec in timesheet:
            rec.write({
                'unit_amount': self.duration,
            })
        return res

    def button_finish(self):
        """ Supering the function of done button to calculate total time in
            timesheet.

            Boolean: Returns true
        """
        res = super(MrpWorkorder, self).button_finish()

        for workorder in self:
            project = self.env['project.project'].search([
                ('name', '=', f"MO: {workorder.production_id.name}")
            ], limit=1)

            task = project.task_ids.search([
                ('name', '=', (
                    f"{workorder.name} in {workorder.workcenter_id.name} for "
                    f"{workorder.product_id.display_name} on {str(workorder.date_start)}"
                ))
            ], limit=1)

            task.write({
                'allocated_hours': workorder.duration_expected
            })

            for rec in task.timesheet_ids:
                rec.write({
                    'unit_amount': workorder.duration,
                })

        return res

    @api.depends('employee_id')
    def _compute_employee_id(self):
        for workorder in self:
               workorder.employee_id = workorder.employee_id
