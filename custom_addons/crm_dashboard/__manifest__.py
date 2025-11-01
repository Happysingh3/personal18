# -*- coding: utf-8 -*-
{
    'name': "CRM Dashboard",
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': """Get a visual report of CRM through a Dashboard in CRM """,
    'description': """CRM dashboard module brings a multipurpose graphical
     dashboard for CRM module and making the relationship management 
     better and easier""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    # ▼▼ ADD: aebo_crm_closing_value (jisme closing_value field define hai)
    'depends': ['crm', 'sale_management', 'aebo_crm_closing_value'],
    'data': [
        'views/crm_dashboard_views.xml',
        'views/res_users_views.xml',
        'views/utm_campaign_views.xml',
        'views/crm_team_views.xml',
        'views/crm_lead_tree_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js',
            'crm_dashboard/static/src/css/style.css',
            'crm_dashboard/static/src/js/crm_dashboard.js',
            'crm_dashboard/static/src/xml/dashboard_templates.xml',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
