
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HrAttendanceBreak(models.Model):
    _name = 'hr.attendance.break'
    _description = 'Attendance Break'
    _order = 'break_in desc'

    attendance_id = fields.Many2one('hr.attendance', required=True, ondelete='cascade', index=True)
    employee_id = fields.Many2one('hr.employee', related='attendance_id.employee_id', store=True, index=True)
    break_in = fields.Datetime(string="Break In", required=True)
    break_out = fields.Datetime(string="Break Out")
    duration = fields.Float(string="Duration (hours)", compute='_compute_duration', store=True)

    @api.depends('break_in', 'break_out')
    def _compute_duration(self):
        for rec in self:
            if rec.break_in and rec.break_out and rec.break_out >= rec.break_in:
                rec.duration = (rec.break_out - rec.break_in).total_seconds() / 3600.0
            else:
                rec.duration = 0.0

    @api.constrains('break_in', 'break_out')
    def _check_bounds(self):
        for rec in self:
            if rec.break_out and rec.break_out < rec.break_in:
                raise ValidationError(_('Break Out cannot be earlier than Break In.'))
            att = rec.attendance_id
            if att and att.check_in:
                if rec.break_in < att.check_in:
                    raise ValidationError(_('Break In must be within the attendance window.'))
                if att.check_out and rec.break_out and rec.break_out > att.check_out:
                    raise ValidationError(_('Break Out must be within the attendance window.'))
