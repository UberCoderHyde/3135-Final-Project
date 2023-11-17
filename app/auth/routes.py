from flask import render_template, request, Blueprint

from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates', url_prefix = "/auth")
@auth.route('/login')
def login():
    return render_template('auth/login.html')