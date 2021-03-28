#Birthday reminder module
##Task description:
Create employees birthday reminder module. Reminder email template model is 'hr.employee'.
Recipients for reminder are records from res.partner model.

Configuration who gets reminder and when, should be in 'hr.department' model or related with it.
There you can choose the number of days to remind before actual birthday. Reminder emails are
sent to all partners that are included in special reminder list (suggestion - create some new model,
or use Odoo current model that best suits such logic where these options would be hold).
If in employee record, birthday field is set and new Boolean field 'Include in Birthday Reminder
List' is checked, then that employee's birthday is included in birthday reminder list.
Also in employee model, there should be two new additional fields: 'Next Birthday' and 'Birthday
Remind Date'. First field should show the date when next birthday is coming up, the other when
birthday reminder will be sent for that employee's next upcoming birthday. Both fields must be
computed fields.

'Next Birthday' depends on standard field 'birthday' and shows next birthday. If next birthday is
today, then it should show the next birthday that comes after this. For example: Employee was born
at '1975-02-03'. Let say today is '2015-02-03', then 'Next Birthday' should be showed as '2016-02-
03'. 'Birthday Remind Date' depends on 'Next Birthday' field and field that lets specify number of
days to send reminder before birthday.

Also these two fields must have search implemented. In other words, you should be able to use
search on employee records using those fields. But 'store=True' can not be used for those fields.
'search' attribute should be used to implement search for non stored computed fields.
Other requirements/notes.

Reminder should be sent once a year at 'Birthday Remind Date' for all partners that are in that
mailing list. Then next year it should be sent the same way only once and not repeat same reminder
etc.

Email template does not have specific requirements. Only that it should understand which language
email template is intended to be used (like field where it knows which language to send). Content of
the reminder template does not matter, only that there should be employee name and its birthday in
email.

Reminders are to be sent automatically by Odoo.
Also if partner is the same one as employee, it should not get a reminder (because he would get
reminder for his own birthday).

## The module in practice:
There will bew new fields in every department that will be sued to set the notification period and the list of employees
to be notified. 

Since it is put in the department, that means that the chosen users must be taken only from the department.
And also every checks must be done on a department level, on who from the department has a birthday's coming up.
Various employees will have the reminder's date field differently calculated based on their department.

Once a day a cronjob will be executed, checking the reminders date and if the employees should et the email or not.
If all checks out then the employee will get an email with a list of upcoming birthdays in N num of days
(depending of the department of the employee)

##Notes:
The idea to put the departments as the settings point is a strange one and confusing. 
In reality what happens is that the HR department gets notified about all employees in the company.
It is safe to say that the settings should be put at the level of the company or a more complex structure to be used,
where in employees it should be chosen which departments(the employees in it) to monitor for birthdays.
