# -*- coding: utf-8 -*-
from odoo import api, fields, models
import re
from decimal import Decimal, InvalidOperation

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # ---------- EXISTING FIELD (AS-IS) ----------
    closing_value_num = fields.Monetary(
        string='Closing Value',
        currency_field='company_currency',
        compute='_compute_closing_value_num',
        store=True,
        readonly=True,
        help='Numeric version of Closing Value for totals and currency formatting.'
    )

    @api.depends('closing_value')
    def _compute_closing_value_num(self):
        number_re = re.compile(r'-?\d+(?:\.\d+)?')
        for rec in self:
            raw = rec.closing_value
            if not raw and raw != 0:
                rec.closing_value_num = 0.0
                continue
            if isinstance(raw, (int, float, Decimal)):
                try:
                    rec.closing_value_num = float(raw)
                except Exception:
                    rec.closing_value_num = 0.0
                continue
            s = str(raw).strip()
            s = s.replace(',', ' ').replace('\xa0', ' ')
            m = number_re.search(s)
            if not m:
                rec.closing_value_num = 0.0
                continue
            token = m.group(0)
            try:
                rec.closing_value_num = float(Decimal(token))
            except (InvalidOperation, ValueError):
                rec.closing_value_num = 0.0

    # ---------- OPTIONAL COLUMNS FOR LIST VIEW (stage-buckets) ----------
    closing_value_so_received = fields.Monetary(
        string='SO Received',
        currency_field='company_currency',
        compute='_compute_stage_closing_buckets',
    )
    closing_value_payment_to_be_received = fields.Monetary(
        string='Delivery Done',  # (caption changed elsewhere for list view)
        currency_field='company_currency',
        compute='_compute_stage_closing_buckets',
    )
    closing_value_payment_received = fields.Monetary(
        string='Payment Received',
        currency_field='company_currency',
        compute='_compute_stage_closing_buckets',
    )

    @api.depends('closing_value_num', 'stage_id')
    def _compute_stage_closing_buckets(self):
        for rec in self:
            amt = rec.closing_value_num or 0.0
            name = (rec.stage_id.name or '').strip().lower()
            rec.closing_value_so_received = amt if name == 'so received' else 0.0
            rec.closing_value_payment_to_be_received = amt if name in ('payment to be received', 'deliverey drone') else 0.0
            rec.closing_value_payment_received = amt if name == 'payment received' else 0.0

    # ---------- FIXED: stage-wise totals with simple SQL SUM ----------
    @api.model
    def get_stage_closing_totals(self, period='month', stage_names=None):
        stage_names = stage_names or ['SO Received', 'Delivery Done', 'Payment Received']
        wanted_norm = [n.strip().lower() for n in stage_names]

        name_to_ids = {}
        for st in self.env['crm.stage'].search([]):
            key = (st.name or '').strip().lower()
            if key in wanted_norm:
                name_to_ids.setdefault(key, []).append(st.id)

        start_dt = fields.Datetime.to_datetime(self._period_start(period or 'month'))

        out = {n: 0.0 for n in stage_names}
        for original_name, norm in zip(stage_names, wanted_norm):
            ids = name_to_ids.get(norm, [])
            if not ids:
                out[original_name] = 0.0
                continue
            ids_tuple = tuple(ids)
            query = """
                SELECT COALESCE(SUM(closing_value_num), 0)
                FROM crm_lead
                WHERE create_date >= %s
                  AND stage_id IN %s
            """
            self.env.cr.execute(query, (start_dt, ids_tuple))
            total = self.env.cr.fetchone()[0] or 0.0
            out[original_name] = float(total)
        return out

    # ---------- NEW: Tender team ke liye Payment Received total ----------
    @api.model
    def get_team_stage_closing_total(self, period='month', team_name='Tender', stage_name='Payment Received'):
        """
        Return float total of closing_value_num for leads of a given Sales Team
        and Stage within the selected period.
        """
        team_ids = self.env['crm.team'].search([('name', 'ilike', team_name)]).ids
        if not team_ids:
            return 0.0
        stage_ids = self.env['crm.stage'].search([('name', 'ilike', stage_name)]).ids
        if not stage_ids:
            return 0.0

        start_dt = fields.Datetime.to_datetime(self._period_start(period or 'month'))

        query = """
            SELECT COALESCE(SUM(closing_value_num), 0)
            FROM crm_lead
            WHERE create_date >= %s
              AND team_id IN %s
              AND stage_id IN %s
        """
        self.env.cr.execute(query, (start_dt, tuple(team_ids), tuple(stage_ids)))
        total = self.env.cr.fetchone()[0] or 0.0
        return float(total)
