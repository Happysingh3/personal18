# -*- coding: utf-8 -*-
###############################################################################

###############################################################################
{
    'name': 'Employee Badge or Card Free',
    'version': '18.0.1.0.1',
    'category': 'HR',
    'summary': """Odoo Employee Badge is new template card or gadge for employee""",
    'description': """Odoo Employee Badge is new template card or gadge for employee""",
    'author': 'V Technologies',
    'company': 'V Technologies',
    'maintainer': 'V Technologies',
    'website': 'https://apps.odoo.com/apps/browse?repo_maintainer_id=599555',
    # 'price': '50',
    # 'currency': 'USD',
    'depends': ['hr'],
    'license': 'LGPL-3',
    'data': [

        'data/paperformat_cr80.xml',
        # 'views/vitouhr_employee_inherit_badge.xml',
        'views/vitouhr_employee_inherit_form.xml',
        'report/vitouhr_employee_badge_portrait_cr80.xml',
        'views/vitouhr_res_company_inherit_form.xml',



    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    "application": False,
}
