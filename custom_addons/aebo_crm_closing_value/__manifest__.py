{
    'name': 'Aebo CRM Closing Value',
    'version': '1.0.0',
    'summary': 'Adds Closing Value field and dropdown menu on CRM Lead form',
    'depends': ['crm', 'product', 'base', 'mail'],  # product depends for product submenu etc.
    'data': [
        'security/assignee_rules.xml',
        'views/crm_lead_search_views.xml',
        'views/crm_lead_views.xml',
        'views/crm_lead_kanban_views.xml',
        'views/crm_lead_quick_create_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'aebo_crm_closing_value/static/src/scss/kanban_blink.css',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
