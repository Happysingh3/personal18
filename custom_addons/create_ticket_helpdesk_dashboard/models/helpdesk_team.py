from odoo import models


class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"

    def _determine_user_to_assign(self):
        """Inherit method to set the default values in the 'Assigned to'
        field # T6382"""
        res = super()._determine_user_to_assign()
        for key, vals in res.items():
            # Check and set the values in user_id if not exist # T6382
            if not vals:
                res[key] = self.env.user
        return res
