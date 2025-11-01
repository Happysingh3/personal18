# -*- coding: utf-8 -*-
{
    "name": "Aebo MessagingMenu: Mark All Read (v6.1)",
    "version": "18.0.6.1",
    "author": "AeboCode",
    "depends": ["mail", "web"],
    "assets": {
        "web.assets_backend": [
            "aebo_messagingmenu_mark_all_v6_1/static/src/js/messaging_menu_mark_all.js"
        ]
    },
    "data": [
        "security/acls.xml"
    ],
    "license": "LGPL-3",
    "summary": "Fix: no needaction field queries; handles discuss.channel.member or mail.channel.partner; auto-refresh UI.",
    "installable": True,
    "application": False
}