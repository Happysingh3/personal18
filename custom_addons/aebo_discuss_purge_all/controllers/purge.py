# controllers/purge.py
import json
from odoo import http
from odoo.http import request

class AeboDiscussPurge(http.Controller):
    @http.route("/aebo_discuss/purge", type="http", methods=["POST"], auth="user", csrf=False)
    def purge(self, **kw):
        raw = request.httprequest.data or b"{}"
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except Exception:
            data = {}
        channel_id = data.get("channel_id") or kw.get("channel_id")
        if not channel_id:
            return request.make_response(json.dumps({"error":"missing channel_id"}), headers=[("Content-Type","application/json")])
        ch = request.env["discuss.channel"].browse(int(channel_id))
        ch.action_aebo_purge()
        return request.make_response(json.dumps({"ok": True}), headers=[("Content-Type","application/json")])