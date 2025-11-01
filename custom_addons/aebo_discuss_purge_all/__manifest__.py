
# -*- coding: utf-8 -*-
{
    "name": "AEBO Discuss: Purge Chat For Everyone",
    "version": "18.0.3.3",
    "summary": "Discuss header Trash button to permanently delete a chat (messages + attachments) for all members",
    "author": "Aebocode",
    "depends": ["mail", "web"],
    "data": [
        "security/ir.model.access.csv",
    ],
    "assets": {
        "web.assets_backend": [
            "aebo_discuss_purge_all/static/src/js/discuss_header_purge.js",
            "aebo_discuss_purge_all/static/src/xml/discuss_header.xml",
        ]
    },
    "license": "LGPL-3",
    "installable": True
}
