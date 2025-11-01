# -- coding: utf-8 --

from odoo import models, fields, api


class ResUsers(models.Model):   
    _inherit = 'res.users'
    
    @api.model_create_multi
    def create(self, vals_list):
        users = super(ResUsers, self).create(vals_list)
        events = self.env['resource.calendar.leaves'].search([('abp_calendar_event','!=',False)]).abp_calendar_event
        
        for user in users:
            if user.partner_id:
                for event in events:
                    event.write({'partner_ids': [(4, user.partner_id.id)] })
        
        return users
    
    
    
    