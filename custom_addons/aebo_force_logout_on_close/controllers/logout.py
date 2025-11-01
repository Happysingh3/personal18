
# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request

class AeboForceLogout(http.Controller):

    @http.route("/aebo_force_logout/logout", type="http", methods=["POST"], auth="user", csrf=False)
    def logout(self, **kw):
        try:
            request.session.logout(keep_db=True)
        except Exception:
            pass
        return request.make_response(json.dumps({"ok": True}), headers=[("Content-Type","application/json")])
