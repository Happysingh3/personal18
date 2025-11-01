# -*- coding: utf-8 -*-
{
    "name": "Aebo Discuss: Clear All (Final)",
    "version": "18.0.5.0",
    "author": "AeboCode",
    "depends": ["mail", "web"],
    "assets": {
        "web.assets_backend": [
            "aebo_discuss_clear_all/static/src/js/inject_clear_next_to_newmsg.js"
        ]
    },
    "data": [
        "security/acls.xml"
    ],
    "license": "LGPL-3",
    "summary": "Adds a Clear button right next to New Message in the Messaging panel; one-click mark-all-read.",
    "installable": True,
    "application": False
}