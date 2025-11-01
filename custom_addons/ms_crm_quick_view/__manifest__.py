# -*- coding: utf-8 -*-

###############################################################################
#
#    MindSynth Technologies
#    Innovative Solutions, Sustainable Growth
#
#    Copyright (C) 2024-TODAY MindSynth Technologies (<https://www.mindsynthtech.com>)
#    Author: MindSynth Technologies (info@mindsynthtech.com)
#
#    This program is free software: you can modify it under the terms of the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#    See the GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': "CRM Lead Quick Preview",

    'summary': "This module allow users to have a quick view of lead details from kanban or pipeline view.",

    'description': """
        This module allow users to have a quick view of lead details from kanban or pipeline view.
    """,

    'author': "MindSynth Technologies",
    'website': "https://www.mindsynthtech.com",
    'category': 'Sales/CRM',
    'version': '18.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm'],

    # always loaded
    'data': [
        'views/crm_lead.xml',
    ],
    'images': [
        'static/description/app-banner.jpg'
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
