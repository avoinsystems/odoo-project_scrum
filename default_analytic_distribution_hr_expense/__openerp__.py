# -*- coding: utf-8 -*-
# © 2016 Pierre Faniel
# © 2016 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Analytic Distribution - Default By Employee',
    'category': 'Accounting & Finance',
    'summary': 'Set a default analytic distribution for each employee',
    'website': 'https://www.niboo.be/',
    'version': '9.0.1.0.0',
    'description': '''
This module allows you to set a default analytic distribution for each
employee. The default analytic distribution will automatically set the
distribution on his expenses.
    ''',
    'author': 'Niboo',
    'depends': [
        'account_analytic_distribution',
    ],
    'data': [
        'views/hr_employee.xml',
    ],
    'installable': True,
    'application': False,
}
