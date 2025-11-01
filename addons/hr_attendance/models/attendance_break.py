# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class HrAttendanceBreak(models.Model):
    _name = "hr.attendance.break"
    _description = "Attendance Breaks"
    _order = "check_in desc, id desc"

    employee_id  = fields.Many2one("hr.employee", required=True, index=True, ondelete="cascade")
    attendance_id = fields.Many2one("hr.attendance", index=True, ondelete="cascade")
    check_in     = fields.Datetime("Break In", required=True, default=fields.Datetime.now)
    check_out    = fields.Datetime("Break Out")
    duration     = fields.Float("Break Duration (hours)", compute="_compute_duration", store=True)
    state        = fields.Selection([('open', 'Open'), ('done', 'Done')], compute="_compute_state", store=True)
    in_latitude  = fields.Float("In Latitude", digits=(10, 7), readonly=True)
    in_longitude = fields.Float("In Longitude", digits=(10, 7), readonly=True)
    out_latitude  = fields.Float("Out Latitude", digits=(10, 7), readonly=True)
    out_longitude = fields.Float("Out Longitude", digits=(10, 7), readonly=True)

    @api.depends('check_out')
    def _compute_state(self):
        for rec in self:
            rec.state = 'done' if rec.check_out else 'open'

    @api.constrains('employee_id')
    def _check_single_open_break(self):
        for rec in self:
            open_break = self.search_count([
                ('employee_id', '=', rec.employee_id.id),
                ('id', '!=', rec.id),
                ('check_out', '=', False),
            ])
            if open_break:
                raise UserError(_("You already have an open break. Please Break Out first."))

    @api.depends('check_in', 'check_out')
    def _compute_duration(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                delta = rec.check_out - rec.check_in
                rec.duration = round(delta.total_seconds() / 3600.0, 2)
            else:
                rec.duration = 0.0
