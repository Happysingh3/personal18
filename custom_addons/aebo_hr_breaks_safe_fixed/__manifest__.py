
# -*- coding: utf-8 -*-
{
    'name': 'Aebo Breaks for Attendance (Safe)',
    'summary': 'Separate systray for Break In / Break Out + stores breaks & shows in Overview (safe dropdown)',
    'version': '1.1.0',
    'category': 'Human Resources/Attendances',
    'depends': ['hr_attendance', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_attendance_break_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'aebo_hr_breaks_safe/static/src/xml/systray_breaks.xml',
            'aebo_hr_breaks_safe/static/src/js/systray_breaks.js',
            'aebo_hr_breaks_safe/static/src/css/systray_breaks.css',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
