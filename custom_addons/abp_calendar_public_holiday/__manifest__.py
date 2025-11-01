# -*- coding: utf-8 -*-
{
    'name': 'Public Holiday on Calendar',
    'category': 'Human Resources',
    'version': '1.0',
    'summary': """This module allows you to view the public holidays declared in the "Time Off" Apps within the Calendar Apps.""",
    'description': """
    This module applies automatically a holiday for all employees in the company
    """,
    'author': 'Ability Partners',
    'company': 'Ability Partners',
    'maintainer': 'Ability Partners',
    'website': 'https://ability-partners.fr',
    'depends': ['hr_holidays'],
    'data': [
        'views/calendar_event_views.xml',
        'views/resource_calendar_leaves_views.xml',
    ],
    'images' : ['static/description/banner.png'],
    'license' : 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}