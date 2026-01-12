# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GradeLevel(models.Model):
    _name = 'grade.level'
    _description = 'Grade Level'
    _order = 'salary_grade_id, level'

    salary_grade_id = fields.Many2one(
        comodel_name='salary.grade',
        string='Salary Grade',
        required=True,
        ondelete='cascade',
        help='The salary grade this level belongs to'
    )
    level = fields.Selection(
        selection=[
            ('A', 'Level A'),
            ('B', 'Level B'),
            ('C', 'Level C'),
            ('D', 'Level D'),
        ],
        string='Level',
        required=True,
        help='Grade level (A/B/C/D)'
    )
    basic_salary = fields.Monetary(
        string='Basic Salary',
        required=True,
        digits='Payroll',
        currency_field='currency_id',
        help='Base salary amount for this level'
    )
    allowances = fields.Monetary(
        string='Allowances',
        default=0.0,
        digits='Payroll',
        currency_field='currency_id',
        help='Additional allowances for this level'
    )
    total_salary = fields.Monetary(
        string='Total Salary',
        compute='_compute_total_salary',
        store=True,
        digits='Payroll',
        currency_field='currency_id',
        help='Total salary (Basic + Allowances)'
    )
    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True,
        help='Display name for the grade level'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Set to false to archive the grade level'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Currency for salary amounts'
    )

    _sql_constraints = [
        (
            'unique_grade_level',
            'UNIQUE(salary_grade_id, level)',
            'This level already exists for the selected salary grade!'
        )
    ]

    @api.depends('basic_salary', 'allowances')
    def _compute_total_salary(self):
        """Compute total salary as sum of basic salary and allowances"""
        for record in self:
            record.total_salary = record.basic_salary + record.allowances

    @api.depends('salary_grade_id', 'level')
    def _compute_name(self):
        """Compute display name from grade and level"""
        for record in self:
            if record.salary_grade_id and record.level:
                record.name = f"{record.salary_grade_id.name} - Level {record.level}"
            else:
                record.name = _('New Grade Level')

    @api.constrains('basic_salary', 'allowances')
    def _check_positive_amounts(self):
        """Ensure salary and allowances are not negative"""
        for record in self:
            if record.basic_salary < 0:
                raise ValidationError(_('Basic salary cannot be negative!'))
            if record.allowances < 0:
                raise ValidationError(_('Allowances cannot be negative!'))

    def name_get(self):
        """Custom display name"""
        result = []
        for record in self:
            if record.salary_grade_id and record.level:
                name = f"{record.salary_grade_id.code} - Level {record.level}"
            else:
                name = _('New Grade Level')
            result.append((record.id, name))
        return result
