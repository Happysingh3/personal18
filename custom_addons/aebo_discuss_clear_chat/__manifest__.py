{
    "name": "Aebo Discuss: Clear Chat",
    "version": "18.0.1.0",
    "category": "Discuss",
    "summary": "Add a 'Clear chat' button to delete all messages & attachments in a DM",
    "depends": ["mail", "bus", "web"],
    "data": [
        "security/aebo_clear_chat_groups.xml",
        "security/ir.model.access.csv",
        "views/assets.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "aebo_discuss_clear_chat/static/src/js/clear_chat.js"
        ]
    },
    "license": "LGPL-3"
}
