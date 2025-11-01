{
    "name": "Sticky Notes",
    "version": "1.0",
    "depends": ["base", "web"],
    "category": "Productivity",
    "license": "LGPL-3",
    "website": "https://vayasoft.com",  # ✅ Add a real or placeholder website
    "author": "Vayasoft",  # ✅ Add author info
    "maintainer": "Vayasoft",  # ✅ Optional but good
    "application": True,
    "summary": "Add sticky notes to any record in Odoo, Keep track, note, logs,chat reminders",
    "data": [
        "security/ir.model.access.csv",
        # "views/note_sticky_views.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "vs_sticky_notes/static/src/js/form_renderer.js",
            "vs_sticky_notes/static/src/js/vs_sticky_note_button.js",
            "vs_sticky_notes/static/src/css/sticky_note.css",
            "vs_sticky_notes/static/src/xml/vs_sticky_note_templates.xml"
        ]
    },
    'images': [
        'static/description/banner.jpg',
    ],
    "installable": True,
    "auto_install": False
}