# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SalaryGrade(models.Model):
    _name = 'salary.grade'
    _description = 'Salary Grade'
    _order = 'sequence, name'

    name = fields.Char(
        string='Grade Name',
        required=True,
        translate=True,
        help='Name of the salary grade'
    )
    code = fields.Char(
        string='Grade Code',
        required=True,
        help='Unique code for the salary grade'
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Order of display'
    )
    grade_level_ids = fields.One2many(
        comodel_name='grade.level',
        inverse_name='salary_grade_id',
        string='Grade Levels',
        help='Levels associated with this salary grade'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Set to false to archive the salary grade'
    )
    level_count = fields.Integer(
        string='Number of Levels',
        compute='_compute_level_count',
        store=True
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'The grade code must be unique!')
    ]

    @api.depends('grade_level_ids')
    def _compute_level_count(self):
        """Compute the number of levels for each grade"""
        for record in self:
            record.level_count = len(record.grade_level_ids)

    def name_get(self):
        """Custom display name"""
        result = []
        for record in self:
            name = f"[{record.code}] {record.name}"
            result.append((record.id, name))
        return result
