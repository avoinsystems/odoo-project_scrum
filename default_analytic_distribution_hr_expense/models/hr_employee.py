# -*- coding: utf-8 -*-
# © 2016 Pierre Faniel
# © 2016 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    analytic_distribution_id = fields.Many2one('account.analytic.distribution',
                                               'Default Analytic Distribution')
