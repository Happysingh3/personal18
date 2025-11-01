
# -*- coding: utf-8 -*-
{
    "name": "AEBO: Auto-Logout When Browser Closes",
    "version": "18.0.1.0",
    "summary": "Automatically log the user out when the last Odoo tab/window is closed",
    "author": "Aebocode",
    "depends": ["web"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "aebo_force_logout_on_close/static/src/js/auto_logout.js",
        ]
    },
    "license": "LGPL-3",
    "installable": True
}
