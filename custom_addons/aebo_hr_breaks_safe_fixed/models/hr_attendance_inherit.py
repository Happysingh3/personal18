
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    break_ids = fields.One2many('hr.attendance.break', 'attendance_id', string="Breaks")
    break_hours = fields.Float(string="Break Hours", compute='_compute_break_hours', store=True)

    @api.depends('break_ids.duration')
    def _compute_break_hours(self):
        for att in self:
            att.break_hours = sum(att.break_ids.mapped('duration'))

    @api.depends('check_in', 'check_out', 'employee_id', 'break_hours')
    def _compute_worked_hours(self):
        super(HrAttendance, self)._compute_worked_hours()
        for att in self:
            if att.worked_hours:
                att.worked_hours = max(att.worked_hours - (att.break_hours or 0.0), 0.0)

    def _get_open_attendance(self, employee):
        return self.search([('employee_id','=',employee.id), ('check_out','=',False)], order='check_in desc', limit=1)

    def action_break_in(self, mode='manual'):
        self.ensure_one()
        if self.check_out:
            raise UserError(_("You are already checked out. Cannot start a break."))
        if self.break_ids.filtered(lambda b: not b.break_out):
            raise UserError(_("A break is already running. Please Break Out first."))
        self.env['hr.attendance.break'].create({
            'attendance_id': self.id,
            'break_in': fields.Datetime.now(),
        })
        return True

    def action_break_out(self, mode='manual'):
        self.ensure_one()
        if self.check_out:
            raise UserError(_("You are already checked out. Cannot stop a break."))
        open_break = self.break_ids.filtered(lambda b: not b.break_out)
        if not open_break:
            raise UserError(_("No running break to stop."))
        open_break.write({'break_out': fields.Datetime.now()})
        return True

    def write(self, vals):
        res = super().write(vals)
        if 'check_out' in vals and vals['check_out']:
            for att in self:
                open_breaks = att.break_ids.filtered(lambda b: not b.break_out)
                if open_breaks:
                    open_breaks.write({'break_out': att.check_out})
        return res
