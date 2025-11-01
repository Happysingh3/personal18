# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2024-TODAY,
#    Author: REAM Vitou (reamvitou@yahoo.com)
#    Tel: +855 17 82 66 82
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class VitouHREmployeeExpiredOnCard(models.Model):
     # _name = 'vitoucms.hr.employee'
     #_inherit = ['mail.thread']
     _inherit = ['hr.employee']
     _description = 'Employee Expired on Card'
     #_rec_name = "provider"
     # _sql_constraints = [
     #      ('name_unique', 'unique(name)', "Currency Code is duplicated!"),
     # ]

     vitouhr_date_joint= fields.Date(string="Date Joint", default=None, store=True)
     # vitouhr_date_expired = fields.Date(string="Card Date Expired", default=None, store=True)
     vitouhr_telephone = fields.Char(string='Telephone', store=True)
     # vitouhr_card_border = fields.Boolean(string='Card Border', default=False, store=True)
     # vitouhr_font_color = fields.Char(string='Font Color (HEX)', store=True, default='#00446e')
     # vitouhr_font_color_company = fields.Char(string='Font Color Company (HEX)', store=True, default='#00446e')
     # vitouhr_bg_top = fields.Binary(string='Bg Top (340x190)', store=True)
     # vitouhr_bg_bottom = fields.Binary(string='Bg Bottom (340x90)', store=True)


     def print_badge_portrait(self):
          return self.open_report_all('vitou_employee_badge_free.vitouhr_print_employee_badge_cr80', 'Print Badge CR80')

     def print_badge_portrait_cr100(self):
          return self.open_report_all('vitou_employee_badge_free.vitouhr_print_employee_badge_cr100', 'Print Badge CR100')


     def open_report_all(self, modulename_reportactionid, reportname):
          return {
               'type': 'ir.actions.report',
               'report_type': 'qweb-pdf',
               'report_name': modulename_reportactionid,
               'report_file': modulename_reportactionid,
               'name': reportname,
          }

     # def action_print_report(self):
     #      return {
     #           'type': 'ir.actions.report',
     #           'report_type': 'qweb-pdf',
     #           'report_name': 'your_module.report_template_id',
     #           'report_file': 'your_module.report_template_id',
     #           'name': 'My Custom Report',
     #      }

     def open_report(self, modulename_reportactionid):
          # self.ensure_one()
          # self.sent = True
          # modulename_reportactionid='vitou_slot_system.it_request_profile_report_template_slot_payout_slip'
          report_action = self.env.ref(modulename_reportactionid)
          # < record id = "it_request_profile_report_template_slot_payout_slip" model = "ir.actions.report" >
          return report_action.report_action(self)

     def open_report_with_record(self, docids, modulename_reportactionid):
          # get the report action back as we will need its data
          # report = self.env['ir.actions.report']._get_report_from_name(module_reportname)
          # get the records selected for this rendering of the report

          # ids = self.get_ids(operationday_id)
          # return self.env['vitouslot.func'].open_report_with_record(ids,'vitou_slot_system.report_template_vitouslot_winloss_report_detail')

          report = self.env.ref(modulename_reportactionid)
          obj = self.env[report.model].browse(docids)
          # print('==>', obj)

          return report.report_action(obj)

#
# def unlink(self):
#      for rec in self:
#           domain = [('type_id', '=', rec.id)]
#           found = self.env['ittechnician.type'].sudo().search(domain)
#           if found:
#                raise ValidationError(_("Invalide this provider. \n there are related to this one" % rec.id))
#           return super().unlink()
