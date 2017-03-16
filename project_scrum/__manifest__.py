# -*- coding: utf-8 -*-
# © 2016 Pierre Faniel
# © 2016 Niboo SPRL (<https://www.niboo.be/>)
# © 2017 Avoin.Systems (<https://avoin.systems/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Project - Scrum',
    'category': "Project",
    'summary': 'Adds the ability to create Sprints and Scrum teams.',
    'website': 'https://avoin.systems/',
    'version': '2.0.0',
    'license': 'AGPL-3',
    'description': """
        This module allows you to organize your tasks with the Scrum methodology. Using sprints, you can easily plan when your tasks should be done.
        """,
    'author': 'Avoin.Systems & Niboo',
    'depends': ['project'],
    'data': [
        'views/project_view.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [],
    'images': [
        'static/description/project_scrum_cover.png',
    ],
    'demo': [
    ],
    'css': [
    ],
    'installable': True,
    'application': False,
}
