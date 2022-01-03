import sqlalchemy.exc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, NumberRange
from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from . import auth
from flask_login import login_user, logout_user, login_required


class RegisterForm(FlaskForm):
    username = StringField('Wprowadź swój username:', validators=[DataRequired(message='Pole nie może być puste')])
    email = StringField('Wprowadź swój adres email:',
                        validators=[DataRequired(message='Pole nie może być puste'), Email()])
    firstname = StringField('Wprowadź swoje imię:', validators=[DataRequired(message='Pole nie może być puste')])
    lastname = StringField('Wprowadź swoje nazwisko:', validators=[DataRequired(message='Pole nie może być puste')])
    phone_number = IntegerField('Wprowadź swój numer telefonu w formacie +xxxxxxxxxxx',
                                validators=[DataRequired(message='Pole nie może być puste'),
                                            NumberRange(10000000000, 99999999999, 'Wprowadź 11 liczb z kodem kraju')])
    password = PasswordField('Wprowadź hasło:', validators=[DataRequired(message='Pole nie może być puste')])
    password2 = PasswordField('Potwierdź hasło:', validators=[DataRequired(message='Pole nie może być puste')])
    submit = SubmitField('Zatwierdź')


class LoginForm(FlaskForm):
    username = StringField('Wprowadź swój nick:', validators=[DataRequired(message='Pole nie może być puste')])
    password = PasswordField('Wprowadź hasło:', validators=[DataRequired(message='Pole nie może być puste')])
    remember_me = BooleanField('Nie wylogowywuj mnie')
    submit = SubmitField('Zaloguj się')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.password2.data:
            password = generate_password_hash(form.password.data)
            user = User(username=form.username.data, password=password,
                        email=form.email.data, firstname=form.firstname.data, lastname=form.lastname.data,
                        phone_number=form.phone_number.data)
            print(user.password)
            try:
                db.session.add(user)
                db.session.commit()
                flash(f'Poprawnie zarejestrowano użytkownika {form.username.data}')
                return redirect('/')
            except sqlalchemy.exc.IntegrityError:
                flash(f'Wystąpił problem')
        else:
            flash("Hasła nie są takie same")
    return render_template('auth.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash(f'Poprawnie zalogowano użytkownika {form.username.data}')
            return redirect('/')
        flash('Niepoprawny nick lub hasło')
    return render_template('auth.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Wylogowałeś się!')
    return redirect('/')
