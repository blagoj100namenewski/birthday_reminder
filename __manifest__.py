# -*- coding: utf-8 -*-
{
    'name': "Birthday Reminders",

    'summary': """
        Module for automatic notifications for upcoming birthdays 
        """,

    'description': """
        Adds employees date of birth, and auto-computes next birthdays. 
        Additionally adds department settings, where users can set up notifications period and list of employees to get them.
        Also includes an email template to be sent.
    """,

    'author': "Blagoj Stoimenovski",
    'website': "https://github.com/blagoj100namenewski",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'views/hr_department.xml',
        'views/hr_employee.xml',
        'data/cron_reminders.xml',
        'data/reminder_email_template.xml',
    ],

}
