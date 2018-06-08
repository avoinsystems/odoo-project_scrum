#
#    Copyright (C) 2017 Avoin Systems (<https://avoin.systems>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from odoo import models, fields


class ReportProjectTaskUser(models.Model):
    # region Private attributes
    _inherit = 'report.project.task.user'
    # endregion

    # region Default methods
    # endregion

    # region Fields declaration
    sprint_id = fields.Many2one(
        'project.scrum.sprint',
        string='Name',
        readonly=True,
    )
    # endregion

    def _select(self):
        # noinspection PyUnresolvedReferences,PyProtectedMember
        select_str = super(ReportProjectTaskUser, self)._select()
        select_str += ", t.sprint_id"
        return select_str

    def _group_by(self):
        # noinspection PyUnresolvedReferences,PyProtectedMember
        group_by_str = super(ReportProjectTaskUser, self)._group_by()
        group_by_str += ", t.sprint_id"
        return group_by_str
