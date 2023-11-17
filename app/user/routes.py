from flask import render_template, request, Blueprint

from flask import Blueprint

user = Blueprint('user', __name__, template_folder='templates',url_prefix="/user")
@user.route('/change_password')
def change_password():
    return render_template('user/change_password.html')

@user.route('/edit_password')
def edit_password():
    return render_template('user/edit_password.html')

@user.route('/profile')
def profile():
    return render_template('user/profile.html')