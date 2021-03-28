# -*- coding: utf-8 -*-
# from odoo import http


# class CustomProjects/birthdayReminder(http.Controller):
#     @http.route('/custom_projects/birthday_reminder/custom_projects/birthday_reminder/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_projects/birthday_reminder/custom_projects/birthday_reminder/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_projects/birthday_reminder.listing', {
#             'root': '/custom_projects/birthday_reminder/custom_projects/birthday_reminder',
#             'objects': http.request.env['custom_projects/birthday_reminder.custom_projects/birthday_reminder'].search([]),
#         })

#     @http.route('/custom_projects/birthday_reminder/custom_projects/birthday_reminder/objects/<model("custom_projects/birthday_reminder.custom_projects/birthday_reminder"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_projects/birthday_reminder.object', {
#             'object': obj
#         })
