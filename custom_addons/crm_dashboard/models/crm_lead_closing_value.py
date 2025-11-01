# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, timedelta

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def _period_start(self, period):
        today = fields.Date.context_today(self)
        if period == 'year':
            return date(today.year, 1, 1)
        if period == 'quarter':
            q = (today.month - 1) // 3
            return date(today.year, q * 3 + 1, 1)
        if period == 'week':
            return today - timedelta(days=today.weekday())  # Monday
        return date(today.year, today.month, 1)  # month (default)

    @api.model
    def get_total_closing_value(self, period='month'):
        """Sum of closing_value for records created in current period.
        Works even if DB column is text.
        """
        start_dt = fields.Datetime.to_datetime(self._period_start(period or 'month'))

        # 1) Fast path if column is numeric
        try:
            domain = [
                ('create_date', '>=', start_dt),
                ('closing_value', '>', 0),
            ]
            data = self.read_group(domain, ['closing_value:sum'], [])
            total = float((data and data[0].get('closing_value_sum')) or 0.0)
            return {'total_closing_value': total}
        except Exception:
            # 2) DB already raised (sum on text). Reset transaction then fallback.
            self.env.cr.rollback()

        # 3) Safe SQL fallback for TEXT columns (remove commas, allow only numeric)
        self.env.cr.execute(
            """
            SELECT COALESCE(
                SUM(
                    CAST(replace(closing_value, ',', '') AS numeric)
                ), 0
            )
            FROM crm_lead
            WHERE create_date >= %s
              AND closing_value IS NOT NULL
              AND btrim(closing_value) <> ''
              AND replace(closing_value, ',', '') ~ '^-?\\d+(\\.\\d+)?$'
            """,
            [start_dt],
        )
        total = self.env.cr.fetchone()[0] or 0
        return {'total_closing_value': float(total)}
