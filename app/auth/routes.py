from flask import render_template, flash, redirect, url_for, request, Blueprint
from app.extensions import db
from .forms import RegistrationForm, LoginForm, ChangePasswordForm
from app.models import User
from flask import Blueprint
from flask_login import current_user, login_required, login_user

auth = Blueprint('auth', __name__, template_folder='templates', url_prefix = "/auth")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Replace 'index' with the name of your homepage route

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('auth/login')

        login_user(user)
        return redirect('/')  # Redirect to the homepage after login
    return render_template('auth/login.html', title='Sign In', form=form)

@auth.route('/register')
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('/login'))  # Redirect to login page after registration
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/reset_password')
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('index'))
        else:
            flash('Invalid old password.')
    return render_template('auth/reset_password.html', title='Change Password', form=form)