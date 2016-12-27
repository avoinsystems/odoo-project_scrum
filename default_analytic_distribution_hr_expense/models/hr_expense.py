# -*- coding: utf-8 -*-
# © 2016 Pierre Faniel
# © 2016 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class HRExpense(models.Model):
    _inherit = 'hr.expense'

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id and self.employee_id.analytic_distribution_ids and\
                not self.analytic_distribution_ids:
            self.analytic_distribution_ids = self.employee_id.\
                analytic_distribution_ids
