# -*- coding: utf-8 -*-

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import datetime


class HRDepartment(models.Model):
    _inherit = 'hr.employee'

    def _search_extra_dates(self, date_name, operator, operand):
        if operator not in ('<', '=', '>', '>=', '<='):
            return []
        # SAME FUNCTION WILL BE USED IN BOTH CASES, SQL STRING WILL VARY
        if date_name == 'next_birthday':
            sql_string = '''
                SELECT id
                FROM hr_employee
                WHERE cast(birthday + ((extract(year from age(birthday)) + 1) * interval '1' year) as date) ''' + operator + ''' '%s' ''' % operand
        else:
            sql_string = '''
                SELECT he.id
                FROM hr_employee he
                INNER JOIN hr_department hd
                ON he.department_id = hd.id
                WHERE cast(he.birthday + ((extract(year from age(he.birthday)) + 1) * interval '1' year) as date) - INTERVAL '1 DAY' * hd.reminder_no_days''' + operator + ''' '%s' ''' % operand

        res = self._cr.execute(sql_string)
        res = self._cr.fetchall()
        if not res:
            return [('id', '=', '0')]
        return [('id', 'in', [r[0] for r in res])]

    @api.model
    def _search_next_birthday(self, operator, operand):
        return self._search_extra_dates('next_birthday', operator, operand)

    @api.model
    def _search_birthday_remind_date(self, operator, operand):
        return self._search_extra_dates('birthday_remind_date', operator, operand)

    # THIS FIELD IS PURELY TO ADD COSMETIC IN THE EMAIL TEMPLATE,
    # TO CALCULATE THE AGE THAT THE EMPLOYEE WILL BE ON HIS BIRTHDAY
    next_age = fields.Integer(compute="_compute_dates")

    include_birthday = fields.Boolean("Include in birthday list")
    birthday = fields.Date()

    next_birthday = fields.Date(compute="_compute_dates", search=_search_next_birthday)
    # REMIND DATE IS CALCULATED DEPENDING ON THE DAYS OF NOTIFICATION IN THE DEPARTMENT OF THE EMPLOYEE
    birthday_remind_date = fields.Date(compute="_compute_dates", search=_search_birthday_remind_date)

    def _compute_dates(self):
        for res in self:
            if res.birthday:
                next_birthday = res.birthday.replace(year=datetime.now().year)
                if next_birthday <= datetime.now().date():
                    next_birthday = next_birthday + relativedelta(years=1)
                res.next_birthday = next_birthday
                res.birthday_remind_date = next_birthday - relativedelta(days=res.department_id.reminder_no_days)
                res.next_age = relativedelta(res.next_birthday, res.birthday).years
            else:
                res.next_birthday = None
                res.birthday_remind_date = None
                res.next_age = None

    @api.model
    def _remind_employees(self):
        # ALL EMPLOYEES THAT HAVE BIRTHDAY UPCOMING,
        # SINCE EVERY DAY THE CRON IS EXECUTED, CHECK IF TODAY IS THE DATE WHEN NOTIFICATIONS
        # ARE TO BE SENT TO THE DEPARTMENT MEMBERS IN THE LIST
        employees = self.search([('birthday_remind_date', '=', datetime.now().date())])
        template = self.env.ref('birthday_reminder.mail_birthday_reminder_template')
        # PUT DEPARTMENT IDS IN TUPLE IN CASE THERE ARE MORE EMPLOYEES WITH THE SAME BIRTHDAY,
        # WE NEED TO ONLY LOOP IT ONCE
        for department in tuple(employees.mapped('department_id')):
            # WE NEED NUM OF EMPLOYEES WITH SAME TODAY'S BIRTHDAY IN THE DEPARTMENT,
            # SO WE CAN CHECK IF THE USER WILL RECEIVE AN EMAIL
            num_employees = len(employees.filtered(lambda x: x.birthday_remind_date == datetime.now().date() and x.department_id == department))
            for remind_employee in department.reminder_employees:
                # IF THERE ARE 2 OR MORE EMPLOYEES WITH TODAY'S BIRTHDAY
                # THEN THE EMPLOYEE THAT IS IN THE REMINDERS LIST IN THE DEPARTMENT WILL ALSO RECEIVE A MESSAGE
                # IF THERE'S ONLY ONE EMPLOYEE THEN THE EMPLOYEE HAS THE BIRTHDAY. SO DON'T SEND AN EMAIL AT ALL
                if remind_employee.birthday_remind_date != datetime.now().date() or num_employees > 1:
                    template.send_mail(remind_employee.id, notif_layout='mail.mail_notification_light', force_send=True)

                #  IN THE TEMPLATE ITSELF, THE LOGIC WILL EXCLUDE THE EMPLOYEE IN THE LIST SHOWING ONLY OTHERS BIRTHDAYS

    def get_birthday_employees(self):

        return self.env['hr.employee'].search([('department_id', '=', self.department_id.id),
                                               ('birthday_remind_date', '=', datetime.now().date()),
                                               ('id', '!=', self.id)

                                               ])


