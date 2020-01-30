# © 2016 Pierre Faniel
# © 2016 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, exceptions, fields, models


class ProjectScrumTeam(models.Model):
    _name = 'project.scrum.team'
    _description = 'Scrum Team'

    name = fields.Char('Name', required=True)
    sprint_ids = fields.One2many('project.scrum.sprint', 'scrum_team_id', 'Sprints')
    project_ids = fields.One2many('project.project', 'scrum_team_id',
                                  'Projects')


class ProjectProject(models.Model):
    _inherit = 'project.project'

    scrum_team_id = fields.Many2one('project.scrum.team', 'Scrum Team')


class ProjectSprint(models.Model):
    _name = 'project.scrum.sprint'
    _description = 'Sprint'

    name = fields.Char('Name', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    scrum_team_id = fields.Many2one('project.scrum.team', 'Scrum Team',
                                    required=True)
    task_count = fields.Integer('# Tasks', compute='_task_count')

    is_current_sprint = fields.Boolean('Is Current Sprint')
    is_previous_sprint = fields.Boolean('Is Previous Sprint')

    def _task_count(self):
        tasks = self.env['project.task'].read_group(
            domain=[('sprint_id', 'in', self.ids)],
            fields=['sprint_id'],
            groupby=['sprint_id'])
        sprint_counts = {group['sprint_id'][0]: group['sprint_id_count'] for group in tasks}
        for sprint in self:
            sprint.task_count = sprint_counts.get(sprint.id, 0)

    @api.constrains("is_current_sprint")
    def check_current_sprint(self):
        self.ensure_one()
        self.check_is_not_both_previous_and_current()
        if self.is_current_sprint:
            old_previous = self.search([('is_previous_sprint', '=', True)])
            if old_previous:
                old_previous.is_previous_sprint = False
            old_current = self.search([
                ('is_current_sprint', '=', True),
                ('id', '!=', self.id),
                ('scrum_team_id', '=', self.scrum_team_id.id),
            ])
            if old_current:
                old_current.is_current_sprint = False
                old_current.is_previous_sprint = True

    @api.constrains("is_previous_sprint")
    def check_previous_sprint(self):
        self.ensure_one()
        self.check_is_not_both_previous_and_current()
        previous_sprints = self.search([
            ('is_previous_sprint', '=', True),
            ('scrum_team_id', '=', self.scrum_team_id.id),
        ])
        if len(previous_sprints) > 1:
            raise exceptions.ValidationError('A single previous sprint is '
                                             'permitted')

    def check_is_not_both_previous_and_current(self):
        self.ensure_one()
        if self.is_current_sprint and self.is_previous_sprint:
            raise exceptions.ValidationError('A sprint cannot be previous'
                                             ' and current at the same time')

    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        for sprint in self:
            concurrent_sprints = self.search([
                '&',
                    '|',
                        '|',
                            '&',
                                ('start_date', '<=', sprint.end_date),
                                ('start_date', '>=', sprint.start_date),
                            '&',
                                ('end_date', '<=', sprint.end_date),
                                ('end_date', '>=', sprint.start_date),
                        '&',
                            ('start_date', '<=', sprint.start_date),
                            ('end_date', '>=', sprint.end_date),
                    '&',
                        ('id', '!=', sprint.id),
                        ('scrum_team_id', '=', sprint.scrum_team_id.id)
            ])
            if concurrent_sprints:
                raise exceptions.ValidationError('Sprints cannot overlap')

    def view_tasks_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'target': 'current',
            'name': self.name,
            'domain': [('sprint_id', '=', self.id)],
            'context': {'default_sprint_id': self.id,}
        }

    _order = "start_date DESC"


class ProjectTask(models.Model):
    _inherit = 'project.task'

    sprint_id = fields.Many2one('project.scrum.sprint', 'Sprint')

    scrum_team_id = fields.Many2one(
        'project.scrum.team',
        'Scrum Team',
        related='sprint_id.scrum_team_id',
    )

    def go_to_sprint_action(self):
        self.ensure_one()
        return self.sprint_id.view_tasks_action()

    def assign_to_me(self):
        self.ensure_one()
        self.user_id = self._uid
