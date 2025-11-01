
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError

class AeboBreaksController(http.Controller):
    @http.route('/hr_attendance/aebo_break_state', type='json', auth='user')
    def aebo_break_state(self):
        employee = request.env.user.employee_id
        att = request.env['hr.attendance']._get_open_attendance(employee)
        if not att:
            return {'checked_in': False, 'current_break_state': 'off', 'break_hours_today': 0.0}
        open_break = att.break_ids.filtered(lambda b: not b.break_out)
        return {'checked_in': True, 'current_break_state': 'on' if open_break else 'off', 'break_hours_today': sum(att.break_ids.mapped('duration'))}

    @http.route('/hr_attendance/break_in', type='json', auth='user')
    def break_in(self):
        employee = request.env.user.employee_id
        att = request.env['hr.attendance']._get_open_attendance(employee)
        if not att:
            raise UserError("You must Check In before starting a break.")
        att.action_break_in(mode='systray')
        return self.aebo_break_state()

    @http.route('/hr_attendance/break_out', type='json', auth='user')
    def break_out(self):
        employee = request.env.user.employee_id
        att = request.env['hr.attendance']._get_open_attendance(employee)
        if not att:
            raise UserError("No active attendance.")
        att.action_break_out(mode='systray')
        return self.aebo_break_state()
