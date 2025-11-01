# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    closing_value = fields.Float("Closing Value")
    stage_closing_date = fields.Date("Stage Closing Date")
    bid_number = fields.Char("Bid Number")
    so_number = fields.Char("SO Number")
    quantity = fields.Integer("Quantity")
    drone_details = fields.Text("Drone Details")
    bid_price = fields.Integer("Bid Price", groups="bid_ra_price.groups_bid_ra_price")
    ra_price = fields.Integer("RA Price", groups="bid_ra_price.groups_bid_ra_price")
    price_confirmed = fields.Char(string="Price Confirmed")
    crac_generated = fields.Char(
        string="CRAC Generated",
        help="Store CRAC generated reference string."
    )
    dropdown_field = fields.Selection([
        ('product', 'Product'),
        ('custom', 'Custom'),
    ], string="Dropdown Menu")

    tender_closing_date = fields.Date("Tender Closing Date")
    product_id = fields.Many2one('product.product', string="Product")

    is_tender_team = fields.Boolean(
        string="Is Tender Team",
        compute="_compute_is_tender_team",
        store=True,
        index=True,
        help="Automatically true when the Sales Team is Tender / Tender-Documentation."
    )

    assignee_ids = fields.Many2many(
        'res.users', 'crm_lead_assignee_rel', 'lead_id', 'user_id',
        string='Assignees',
        help='Additional salespersons assigned to this lead.'
    )

    # ⬇️ सिर्फ़ दो states रखें: overdue / today
    stage_alert = fields.Selection(
        [
            ('overdue', 'Overdue'),
            ('today',   'Due Today'),
        ],
        compute="_compute_stage_alert",
        store=False,
        help="Visual alert for Stage Closing Date on Kanban."
    )

    def action_assign_to_me(self):
        for lead in self:
            if self.env.user not in lead.assignee_ids:
                lead.assignee_ids = [(4, self.env.user.id)]
            partner = self.env.user.partner_id
            if partner and partner not in lead.message_partner_ids:
                lead.message_subscribe([partner.id])

    def _norm(self, s):
        s = (s or '').strip().lower()
        return ' '.join(s.split())

    @api.depends('team_id', 'team_id.name')
    def _compute_is_tender_team(self):
        tender_names = {'tender', 'tender team', 'tender-documentation', 'tender documentation'}
        for rec in self:
            rec.is_tender_team = self._norm(rec.team_id.name) in tender_names

    # ⬇️ “soon” logic हटा दी
    @api.depends('stage_closing_date')
    def _compute_stage_alert(self):
        today = fields.Date.today()
        for rec in self:
            d = rec.stage_closing_date
            if not d:
                rec.stage_alert = False
            elif d < today:
                rec.stage_alert = 'overdue'
            elif d == today:
                rec.stage_alert = 'today'
            else:
                rec.stage_alert = False

    @api.onchange('dropdown_field')
    def _onchange_dropdown_field_clear(self):
        if self.dropdown_field == 'product':
            self.drone_details = False
        elif self.dropdown_field == 'custom':
            self.product_id = False
        else:
            self.product_id = False
            self.drone_details = False

    def _sync_followers_with_assignees(self, added_user_ids=None, removed_user_ids=None):
        for lead in self:
            users_to_add = lead.assignee_ids if added_user_ids is None else self.env['res.users'].browse(added_user_ids)
            partners_to_add = users_to_add.mapped('partner_id').filtered(lambda p: p)
            if partners_to_add:
                lead.message_subscribe(partner_ids=partners_to_add.ids)
            if removed_user_ids:
                partners_to_remove = self.env['res.users'].browse(removed_user_ids).mapped('partner_id').filtered(lambda p: p)
                if partners_to_remove:
                    lead.message_unsubscribe(partner_ids=partners_to_remove.ids)

    @api.model_create_multi
    def create(self, vals_list):
        leads = super().create(vals_list)
        for lead, vals in zip(leads, vals_list):
            assignee_cmds = vals.get('assignee_ids')
            if assignee_cmds:
                new_ids = set()
                for cmd in assignee_cmds:
                    if isinstance(cmd, (list, tuple)) and len(cmd) >= 1:
                        if cmd[0] == 6:
                            new_ids.update(cmd[2] or [])
                        elif cmd[0] == 4:
                            new_ids.add(cmd[1])
                if new_ids:
                    lead._sync_followers_with_assignees(added_user_ids=list(new_ids))
            else:
                if lead.assignee_ids:
                    lead._sync_followers_with_assignees()
        return leads

    def write(self, vals):
        before_map = {lead.id: set(lead.assignee_ids.ids) for lead in self}
        res = super().write(vals)
        if 'assignee_ids' in vals:
            for lead in self:
                before = before_map.get(lead.id, set())
                after = set(lead.assignee_ids.ids)
                added = list(after - before)
                removed = list(before - after)
                if added or removed:
                    lead._sync_followers_with_assignees(
                        added_user_ids=added or None,
                        removed_user_ids=removed or None,
                    )
        return res

    def action_assign_to_me(self):
        for lead in self:
            if self.env.user not in lead.assignee_ids:
                lead.assignee_ids = [(4, self.env.user.id)]
            partner = self.env.user.partner_id
            if partner:
                lead.message_subscribe([partner.id])
