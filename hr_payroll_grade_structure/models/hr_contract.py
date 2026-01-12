# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class HrContract(models.Model):
    _inherit = 'hr.contract'

    salary_grade_id = fields.Many2one(
        comodel_name='salary.grade',
        string='Salary Grade',
        tracking=True,
        help='Select the salary grade for this contract'
    )
    grade_level_id = fields.Many2one(
        comodel_name='grade.level',
        string='Grade Level',
        tracking=True,
        required=False,
        domain="[('salary_grade_id', '=', salary_grade_id)]",
        help='Select the grade level (A/B/C/D)'
    )
    basic_salary = fields.Monetary(
        string='Basic Salary',
        digits='Payroll',
        tracking=True,
        currency_field='currency_id',
        help='Basic salary from the selected grade level'
    )
    allowances = fields.Monetary(
        string='Allowances',
        digits='Payroll',
        tracking=True,
        currency_field='currency_id',
        help='Allowances from the selected grade level'
    )
    
    is_salary_applied = fields.Boolean(
        string='Salary Applied',
        compute='_compute_is_salary_applied',
        store=True,
        help='Indicates if the salary structure has been applied'
    )

    @api.depends('salary_grade_id', 'grade_level_id', 'basic_salary', 'allowances')
    def _compute_is_salary_applied(self):
        for contract in self:
            if not contract.salary_grade_id or not contract.grade_level_id:
                contract.is_salary_applied = False
                continue
                
            # Check if the current values match the grade level values
            grade_level = contract.grade_level_id
            contract.is_salary_applied = (
                contract.basic_salary == grade_level.basic_salary and
                contract.allowances == grade_level.allowances
            )
            
    @api.onchange('salary_grade_id')
    def _onchange_salary_grade_id(self):
        """Clear grade level when salary grade changes"""
        self.grade_level_id = False
        self.basic_salary = 0
        self.allowances = 0
        if self.salary_grade_id:
            return {
                'domain': {
                    'grade_level_id': [('salary_grade_id', '=', self.salary_grade_id.id)]
                }
            }
        else:
            return {
                'domain': {
                    'grade_level_id': [('id', '=', False)]
                }
            }

    @api.constrains('salary_grade_id', 'grade_level_id')
    def _check_grade_level_belongs_to_grade(self):
        """Ensure selected grade level belongs to selected salary grade"""
        for record in self:
            if record.grade_level_id and record.salary_grade_id:
                if record.grade_level_id.salary_grade_id != record.salary_grade_id:
                    raise ValidationError(_(
                        'The selected Grade Level does not belong to the selected Salary Grade!'
                    ))

    def apply_salary_structure(self):
        """Apply salary structure from selected grade level to contract"""
        self.ensure_one()
        
        if not self.salary_grade_id:
            raise UserError(_('Please select a Salary Grade first!'))
        
        if not self.grade_level_id:
            raise UserError(_('Please select a Grade Level first!'))
        
        self.write({
            'basic_salary': self.grade_level_id.basic_salary,
            'wage': self.grade_level_id.total_salary,
            'allowances': self.grade_level_id.allowances, 
        })
        
        self.message_post(
            body=_("Salary structure applied from Grade Level: %s") % self.grade_level_id.display_name
        )
        
        return True
