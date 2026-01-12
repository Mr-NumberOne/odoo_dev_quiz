# -*- coding: utf-8 -*-
{
    'name': 'HR Payroll Grade Structure',
    'version': '17.0.1.0.0',
    'summary': 'Manage salary grades and levels with automatic contract integration',
    'description': """
        HR Payroll Grade Structure
        ===========================
        This module allows you to:
        * Define salary grades with unique codes
        * Create grade levels (A/B/C/D) for each salary grade
        * Set basic salary and allowances for each level
        * Automatically apply salary structures to HR contracts
        * Enforce business constraints for data integrity
    """,
    'author': 'Ahmed Maher Ali Ahmed AL-Maqtari',
    'category': 'Human Resources/Payroll',
    'depends': ['base', 'hr', 'hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/salary_grade_views.xml',
        'views/grade_level_views.xml',
        'views/hr_contract_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
