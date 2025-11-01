# -*- coding: utf-8 -*-
{
    'name': 'Odoo Fullscreen Mode',
    'author': 'Odoo Hub',
    'category': 'Tools',
    'summary': 'Easily toggle fullscreen mode in Odoo with a button in the systray. Boost productivity by maximizing your workspace with a simple click. odoo full screen mode, odoo fullscreen mode, full view, top right corner menu, toggle full screen mode, maximize odoo view, maximize/minimize fullscreen mode',
    'description': """
        This module adds a button to the Odoo system tray (systray) that allows 
        users to toggle fullscreen mode within the Odoo interface. It is designed 
        to provide a more immersive user experience by removing distractions and 
        maximizing the workspace.
    """,
    'maintainer': 'Odoo Hub',
    'version': '1.0',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            'odoo_fullscreen_mode/static/src/**/*',
        ],
    },
    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
