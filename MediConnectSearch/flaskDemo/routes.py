import os
import secrets
# from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import SearchForm,RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required
from flaskDemo.models import User, Doctor, Patient, Person
# from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, DeptForm,DeptUpdateForm,AssignmentUpdateForm, AssignmentForm
# from flaskDemo.models import User, Post,Department, Dependent, Dept_Locations, Employee, Project, Works_On
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/search", methods=['GET', 'POST'])
@login_required
def searchLoggedIn():
    form = SearchForm()
    if form.validate_on_submit():
        results = Person.query.join(Doctor, Doctor.Ssn == Person.Ssn) \
            .filter_by(Specialty=form.specialty.data, Language=form.language.data, CityOfPractice=form.location.data) \
            .add_columns(Doctor.Ssn, Doctor.Specialty, Person.FirstName, Person.LastName, Doctor.CityOfPractice)
        flash('Redirecting you to Search Results!', 'success')
        return render_template('searchResult.html', title='Providers that Match your Search', results=results)
    return render_template('searchLoggedIn.html', title='Provider Search Criteria', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(id=form.user_id.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/account/delete", methods=['POST'])
@login_required
def delete_account():
    user_id = current_user.id
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('home'))


# @app.route("/")
# @app.route("/home")
# def home():
#     assignments = Works_On.query.join(Employee, Works_On.essn == Employee.ssn)\
#                   .add_columns(Works_On.pno, Works_On.essn, Employee.ssn, Employee.lname, Employee.fname)\
#                   .join(Project, Project.pnumber == Works_On.pno).add_columns(Project.pname)
#     return render_template('assign_home.html', outString=assignments)

   
# @app.route("/join")
# def join():
#     results2 = Employee.query.join(Works_On,Employee.ssn == Works_On.essn) \
#                .add_columns(Works_On.essn) \
#                .join(Project,Project.pnumber == Works_On.pno).add_columns(Works_On.pno)
#     return render_template('join.html', title='Join', joined_m_n=results2)


# @app.route("/assign/<essn>/<pno>")
# @login_required
# def assign(essn, pno):
#     assign = Works_On.query.get_or_404([essn,pno])
#     return render_template("assign.html", title=str(assign.essn) + "_" + str(assign.pno), assign=assign, now=datetime.utcnow())
#
#
# @app.route("/assign/<essn>/<pno>delete", methods=['POST'])
# @login_required
# def delete_assignment(essn,pno):
#     assignment = Works_On.query.get_or_404([essn,pno])
#     db.session.delete(assignment)
#     db.session.commit()
#     flash('The assignment has been deleted!', 'success')
#     return redirect(url_for('home'))
#

# @app.route("/assign/<essn>/<pno>update", methods=['GET','POST'])
# @login_required
# def update_assignment(essn,pno):
#     return "update page under construction"


# @app.route("/assign/new", methods=['GET', 'POST'])
# @login_required
# def new_assignment():
#     form = AssignmentForm()
#     if form.validate_on_submit() and form.validate_assignment(form.essn.data):
#         assignment = Works_On(pno=form.pno.data, essn=form.essn.data, hours=form.hours.data)
#         db.session.add(assignment)
#         db.session.commit()
#         flash('You have added a new assignment!', 'success')
#         return redirect(url_for('home'))
#     return render_template('create_assignment.html', title='New Assignment',
#                            form=form, legend='New Assignment')


# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
#
#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)
#
#     return picture_fn


# @app.route("/dept/new", methods=['GET', 'POST'])
# @login_required
# def new_dept():
#     form = DeptForm()
#     if form.validate_on_submit():
#         dept = Department(dname=form.dname.data, dnumber=form.dnumber.data,mgr_ssn=form.mgr_ssn.data,mgr_start=form.mgr_start.data)
#         db.session.add(dept)
#         db.session.commit()
#         flash('You have added a new department!', 'success')
#         return redirect(url_for('home'))
#     return render_template('create_dept.html', title='New Department',
#                            form=form, legend='New Department')


# @app.route("/dept/<dnumber>")
# @login_required
# def dept(dnumber):
#     dept = Department.query.get_or_404(dnumber)
#     return render_template('dept.html', title=dept.dname, dept=dept, now=datetime.utcnow())
#
#
# @app.route("/dept/<dnumber>/update", methods=['GET', 'POST'])
# @login_required
# def update_dept(dnumber):
#     dept = Department.query.get_or_404(dnumber)
#     currentDept = dept.dname
#
#     form = DeptUpdateForm()
#     if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
#         if currentDept !=form.dname.data:
#             dept.dname=form.dname.data
#         dept.mgr_ssn=form.mgr_ssn.data
#         dept.mgr_start=form.mgr_start.data
#         db.session.commit()
#         flash('Your department has been updated!', 'success')
#         return redirect(url_for('dept', dnumber=dnumber))
#     elif request.method == 'GET':              # notice we are not passing the dnumber to the form
#
#         form.dnumber.data = dept.dnumber
#         form.dname.data = dept.dname
#         form.mgr_ssn.data = dept.mgr_ssn
#         form.mgr_start.data = dept.mgr_start
#     return render_template('create_dept.html', title='Update Department',
#                            form=form, legend='Update Department')


# @app.route("/dept/<dnumber>/delete", methods=['POST'])
# @login_required
# def delete_dept(dnumber):
#     dept = Department.query.get_or_404(dnumber)
#     db.session.delete(dept)
#     db.session.commit()
#     flash('The department has been deleted!', 'success')
#     return redirect(url_for('home'))
