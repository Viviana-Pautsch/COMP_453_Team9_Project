from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from flaskDemo.models import User, Doctor, Patient
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
# from wtforms.fields.html5 import DateField


class RegistrationForm(FlaskForm):
    user_id = IntegerField('ID Number', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_user_id(self, user_id):
        user = Doctor.query.filter_by(DoctorID=user_id.data).first()
        user2 = Patient.query.filter_by(PatientID=user_id.data).first()
        if not user and not user2:
            raise ValidationError('That ID number is invalid. Please enter a valid ID Number.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class SearchForm(FlaskForm):
    doctor_specialties = Doctor.query.with_entities(Doctor.Specialty).distinct()
    results = list()
    for row in doctor_specialties:
        rowDict = row._asdict()
        results.append(rowDict)
    specialty_Choices = sorted([(row['Specialty'], row['Specialty']) for row in results])

    language = Doctor.query.with_entities(Doctor.Language).distinct()
    results2 = list()
    for row in language:
        rowDict = row._asdict()
        results2.append(rowDict)
    language_Choices = sorted([(row['Language'], row["Language"]) for row in results2])

    locations = Doctor.query.with_entities(Doctor.CityOfPractice).distinct()
    results3 = list()
    for row in locations:
        rowDict = row._asdict()
        results3.append(rowDict)

    location_Choices = sorted([(row['CityOfPractice'], row['CityOfPractice']) for row in results3])
    specialty = SelectField("Doctor Specialty", choices=specialty_Choices)
    language = SelectField("Language", choices=language_Choices)
    location = SelectField("Location", choices=location_Choices)
    submit = SubmitField('Find a Doctor')

# class AssignmentUpdateForm(FlaskForm):
#
#     essn = SelectField("Employee SSN", choices=emp_Choices)  # myChoices defined at top
#     pno = SelectField("Project Number", choices= project_Choices, coerce=int)
#     hours=IntegerField('Number of Hours Allocated', validators=[DataRequired()])
#     submit = SubmitField('Update this assignment')
#
#     def validate_pno(self, essn):    # apparently in the company DB, dname is specified as unique
#          assignment = Works_On.query.filter_by(essn=essn.data)
#          valid_pnos = list()
#          for instance in assignment:
#             valid_pnos.append(instance.pno)
#          if (int(self.pno.data) not in valid_pnos):
#              raise ValidationError('That project is already being assigned. Please choose a different project.')
#

    
# class DeptUpdateForm(FlaskForm):
#
# #    dnumber=IntegerField('Department Number', validators=[DataRequired()])
#     dnumber = HiddenField("")
#
#     dname=StringField('Department Name:', validators=[DataRequired(),Length(max=15)])
# #  Commented out using a text field, validated with a Regexp.  That also works, but a hassle to enter ssn.
# #    mgr_ssn = StringField("Manager's SSN", validators=[DataRequired(),Regexp('^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$', message="Please enter 9 digits for a social security.")])
#
# #  One of many ways to use SelectField or QuerySelectField.  Lots of issues using those fields!!
#     mgr_ssn = SelectField("Manager's SSN", choices=myChoices)  # myChoices defined at top
#
# # the regexp works, and even gives an error message
# #    mgr_start=DateField("Manager's Start Date:  yyyy-mm-dd",validators=[Regexp(regex)])
# #    mgr_start = DateField("Manager's Start Date")
#
# #    mgr_start=DateField("Manager's Start Date", format='%Y-%m-%d')
#     mgr_start = DateField("Manager's start date:", format='%Y-%m-%d')  # This is using the html5 date picker (imported)
#     submit = SubmitField('Update this department')
#
#
# # got rid of def validate_dnumber
#
#     def validate_dname(self, dname):    # apparently in the company DB, dname is specified as unique
#          dept = Department.query.filter_by(dname=dname.data).first()
#          if dept and (str(dept.dnumber) != str(self.dnumber.data)):
#              raise ValidationError('That department name is already being used. Please choose a different name.')


# class AssignmentForm(FlaskForm):
#
#     # essn = StringField("Employee SSN")  # myChoices defined at top
#     essn = StringField("Employee SSN")  # myChoices defined at top
#     pno = SelectField("Project Number", choices= project_Choices, coerce=int)
#     hours=IntegerField('Number of Hours Allocated', validators=[DataRequired()])
#     submit = SubmitField('Add this assignment')
#     #def validate_assignment(self, essn, pno):    # apparently in the company DB, dname is specified as unique
#         #assignment = Works_On.query.all()
#         #for instance in assignment:
#            #if (instance.pno == self.pno and instance.essn == self.essn) == False:
#             #raise ValidationError('This assignment already exists. Please choose a different assignment.')
#
#     def validate_assignment(self, essn):    #because dnumber is primary key and should be unique
#         emp_assignments = Works_On.query.filter_by(essn=essn)
#         for assignment in emp_assignments:
#             if(str(self.pno.data) == str(assignment.pno)):
#                 raise ValidationError('That Assignment already exists. Please choose a different one.')
#                 return False



    # # essn = StringField("Employee SSN")  # myChoices defined at top
    # essn = StringField("Employee SSN")  # myChoices defined at top
    # pno = SelectField("Project Number", choices=project_Choices, coerce=int)
    # hours = IntegerField('Number of Hours Allocated', validators=[DataRequired()])
    # submit = SubmitField('Add this assignment')
    #
    # # def validate_assignment(self, essn, pno):    # apparently in the company DB, dname is specified as unique
    # # assignment = Works_On.query.all()
    # # for instance in assignment:
    # # if (instance.pno == self.pno and instance.essn == self.essn) == False:
    # # raise ValidationError('This assignment already exists. Please choose a different assignment.')
    #
    # def validate_assignment(self, essn):  # because dnumber is primary key and should be unique
    #     emp_assignments = Works_On.query.filter_by(essn=essn)
    #     for assignment in emp_assignments:
    #         if (str(self.pno.data) == str(assignment.pno)):
    #             raise ValidationError('That Assignment already exists. Please choose a different one.')
    #             return False

# class DeptForm(DeptUpdateForm):
#
#     dnumber=IntegerField('Department Number', validators=[DataRequired()])
#     submit = SubmitField('Add this department')
#
#     def validate_dnumber(self, dnumber):    #because dnumber is primary key and should be unique
#         dept = Department.query.filter_by(dnumber=dnumber.data).first()
#         if dept:
#             raise ValidationError('That department number is taken. Please choose a different one.')

