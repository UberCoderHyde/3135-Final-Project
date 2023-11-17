from flask import render_template, request, Blueprint

from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates', url_prefix = "/auth")
@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/register')
def register():
    return render_template('auth/register.html')

@auth.route('/reset_password')
def reset_password():
    return render_template('auth/reset_password.html')