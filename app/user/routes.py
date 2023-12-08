from .forms import EditProfileForm
from flask import flash, redirect, render_template, request, Blueprint, url_for
from flask_login import current_user, login_required
from app.models import User
from flask import Blueprint
from app.extensions import db

user = Blueprint('user', __name__, template_folder='templates',url_prefix="/user")

@user.route('/profile/<int:user_id>')
def user_profile(user_id):
    tutor = User.query.get_or_404(user_id)
    return render_template('user/profile.html', user=user)
@user.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.description = form.description.data
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('user.user_profile', user_id=current_user.id))
    
    elif request.method == 'GET':
        form.description.data = current_user.description
    return render_template('user/edit_profile.html', form=form)