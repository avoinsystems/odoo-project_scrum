# -*- coding: utf-8 -*-
# © 2016 Jérôme Guerriat
# © 2016 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, exceptions, fields, models


class PublicHoliday(models.Model):
    _name = "hr.public_holiday"

    date = fields.Date("Public Holiday Date", required=True)
    company_id = fields.Many2one('res.company', string="Company", required=True)
    name = fields.Char(string="Holiday Name", required=True)

    @api.multi
    def create_leaves(self):
        self.ensure_one()
        HRHolidays = self.env['hr.holidays']
        holiday_status_id = self.env['hr.holidays.status'].search(
            [('is_public_holiday', '=', True)])
        employee_ids = self.env['hr.employee'].search(
            [('company_id', '=', self.company_id.id)])
        values = {'name': self.name,
                  'type': 'remove',
                  'holiday_type': 'employee',
                  'holiday_status_id': holiday_status_id.id,
                  'date_from': self.date,
                  'date_to': self.date,
                  'number_of_days_temp': 1,
                  'state': 'validate',
                  }

        error_list = []
        for employee in employee_ids:
            values['employee_id'] = employee.id
            try:
                # TODO find proper context call to send email with next wave instead of immediately
                HRHolidays.with_context(for_sent=False).create(values)
            except Exception, e:
                error_list.append('%s: %s\n' % (employee.name, e))

        if error_list:
            raise exceptions.ValidationError('The following errors were raised' % error_list)

    @api.multi
    def remove_leaves(self):
        self.ensure_one()
        employee_ids = self.env['hr.employee'].search(
            [('company_id', '=', self.company_id)])

    _sql_constraints = [
        ('unique_date',
         'UNIQUE (date, company_id)',
         'You should only have one public holiday per company and date')
    ]


class HRHolidaysStatus(models.Model):
    _inherit = 'hr.holidays.status'

    is_public_holiday = fields.Boolean('Public Holiday')

    @api.multi
    @api.constrains('is_public_holiday')
    def check_unique_public_holiday(self):
        for holiday_status in self:
            if self.env['hr.holidays.status'].search(
                    [('is_public_holiday', '=', True),
                     ('id', '!=', holiday_status.id)]).ids:
                raise exceptions.ValidationError('You can only have one leave type set as Public Holiday')
