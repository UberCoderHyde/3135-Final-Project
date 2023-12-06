from flask import render_template, redirect, url_for
from app import app  #Flask app
from .forms import EditProfileForm, EditUserProfileForm, ProfileForm

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        # Process the form data, update the user profile, and redirect
        return redirect(url_for('profile'))  # Redirect to the profile page

    return render_template('edit_profile.html', form=form)

@app.route('/edit_user_profile', methods=['GET', 'POST'])
def edit_user_profile():
    form = EditUserProfileForm()

    if form.validate_on_submit():
        # Process the form data, update the user profile, and redirect
        return redirect(url_for('profile'))  # Redirect to the profile page

    return render_template('edit_user_profile.html', form=form)

@app.route('/profile')
def profile():
    # Fetch user data from your database or user authentication system
    user = get_user_data()  # Replace with your method to get user data
    return render_template('profile.html', user=user)