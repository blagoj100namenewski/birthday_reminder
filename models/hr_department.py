# -*- coding: utf-8 -*-

from odoo import fields, models


class HRDepartment(models.Model):
    _inherit = 'hr.department'

    reminder_no_days = fields.Integer("No. days before reminder", default=1)
    reminder_employees = fields.Many2many('hr.employee', string="List of employees for reminder", domain="[('department_id', '=', id)]")
