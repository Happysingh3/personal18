# -*- coding: utf-8 -*-
from odoo import models, api, fields
from datetime import datetime, time

class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            emp = rec.employee_id
            if not emp:
                continue

            check_dt = fields.Datetime.to_datetime(rec.check_in)
            if not check_dt:
                continue

            if self._is_public_holiday(emp, check_dt):
                day_start = datetime.combine(fields.Date.to_date(check_dt), time.min)
                day_end   = datetime.combine(fields.Date.to_date(check_dt), time.max)

                if not self._has_cpl_for_day(emp, day_start, day_end):
                    self._create_cpl_allocation(emp, check_dt, day_start, day_end)
        return records

    def _is_public_holiday(self, employee, dt):
        CalendarLeave = self.env["resource.calendar.leaves"]
        domain = [
            ("date_from", "<=", dt),
            ("date_to",   ">=", dt),
            "|", ("calendar_id", "=", employee.resource_calendar_id.id or False),
                 ("calendar_id", "=", False),
            "|", ("resource_id", "=", employee.resource_id.id or False),
                 ("resource_id", "=", False),
            "|", ("company_id", "=", employee.company_id.id if employee.company_id else False),
                 ("company_id", "=", False),
        ]
        leaves = CalendarLeave.search(domain, limit=1)
        return bool(leaves)

    def _has_cpl_for_day(self, employee, day_start, day_end):
        Allocation = self.env["hr.leave.allocation"]
        cpl_type = self._get_cpl_leave_type()
        if not cpl_type:
            return False
        domain = [
            ("employee_id", "=", employee.id),
            ("holiday_status_id", "=", cpl_type.id),
            ("state", "in", ["draft", "confirm", "validate", "validate1"]),
            "|", "&", ("date_from", "<=", day_end), ("date_to", ">=", day_start),
                 "&", ("date_from", "=", False), ("date_to", "=", False),
        ]
        return bool(Allocation.search(domain, limit=1))

    def _get_cpl_leave_type(self):
        LeaveType = self.env["hr.leave.type"]
        # Hard-coded to your environment's leave type name:
        return LeaveType.search([("name", "=", "Compensatory Days")], limit=1)

    def _create_cpl_allocation(self, employee, check_dt, day_start, day_end):
        Allocation = self.env["hr.leave.allocation"]
        cpl_type = self._get_cpl_leave_type()
        if not cpl_type:
            return

        vals = {
            "name": f"CPL for {fields.Date.to_date(check_dt)}",
            "holiday_status_id": cpl_type.id,
            "employee_id": employee.id,
            "date_from": day_start,
            "date_to": day_end,
            "allocation_type": "regular",
            "state": "confirm",
        }

        # If your type is hours-based, default to 8 hours; else 1 day.
        if getattr(cpl_type, "request_unit", "day") == "hour":
            vals["number_of_days"] = 0.0
            vals["number_of_hours_display"] = 8.0
        else:
            vals["number_of_days"] = 1.0

        Allocation.create(vals)
