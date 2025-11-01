# -*- coding: utf-8 -*-
{
    'name': 'Recycle Bin',
    'category': 'Tools',
    'author': 'Scott Weber',
    'summary': 'The Recycle Bin module is a data recovery tool for Odoo that ensures deleted records are safely stored and can be easily restored. It logs details of the deleted data, including relationships and hierarchies, allowing seamless recovery of both primary and related records.',
    'website': 'https://odooforge.com/recycle-bin',
    "application":True,
    'category': 'Sales',
    'version': '18.1',
    'maintainer': 'Odoo Forge',
    'license': 'AGPL-3',
    'support': 'info@odooforge.com',
    'description': """
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/recycle_bin_views.xml',
        'data/scheduledaction.xml',
        'views/config_settings.xml',
    ],
    'images': ['static/description/cover.gif'],
    "assets": {
        "web.assets_frontend": [
            "static/src/index.html",
        ],
    },
    # 'demo': [
    #     'data/demo_data.xml',  
    # ],
    "installable": True,
    
}
