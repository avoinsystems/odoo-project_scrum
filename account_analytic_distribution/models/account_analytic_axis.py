# -*- coding: utf-8 -*-
# © 2015 Jérôme Guerriat, Pierre Faniel
# © 2015 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import exceptions, fields, models


class AccountAnalyticAxis(models.Model):

    _name = 'account.analytic.axis'
    _description = 'Analytic axis'

    name = fields.Char('Axis name')
    active = fields.Boolean('Active', default=True)
    analytic_account_ids = fields.One2many('account.analytic.account',
                                           'analytic_account_axis_id',
                                           'Analytic Accounts')
    mandatory = fields.Boolean('Mandatory')

    def check_percent_on_axis(self, distributions):
        mandatory_axis = self.env['account.analytic.axis'].search(
            [('mandatory', '=', True)])
        distribution_by_axis = {}
        for axis in mandatory_axis:
            distribution_by_axis.setdefault(axis, [])
        for distribution in distributions:
            axis = distribution.analytic_account_id.analytic_account_axis_id
            distribution_by_axis.setdefault(axis, [])
            distribution_by_axis[axis].append(distribution)

        message = ''
        for axis, distributions in distribution_by_axis.iteritems():
            try:
                axis._check_percent_on_axis(distributions)
            except exceptions.ValidationError, e:
                message += e.name

        if message:
            raise exceptions.ValidationError(message)
        return True

    def _check_percent_on_axis(self, distributions):
        total = sum(distribution.rate for distribution in distributions)
        total = round(total, 2)
        if total != 100.0 and total != 0.0:
            raise exceptions.ValidationError(
                'Axis %s has a total distribution of %s%% \n' %
                (self.name, total))
        if self.mandatory and total != 100.0:
            raise exceptions.ValidationError(
                'Axis %s must have a total distribution of 100%% '
                '(Currently: %s)\n' % (self.name, total))
