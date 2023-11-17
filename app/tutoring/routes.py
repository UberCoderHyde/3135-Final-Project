from flask import render_template, request, Blueprint

from flask import Blueprint

tutoring = Blueprint('tutoring', __name__, template_folder='templates',url_prefix="/tutoring")
@tutoring.route('/list_tutors')
def list_tutors():
    return render_template('tutoring/list_tutors.html')

@tutoring.route('/tutor_profile')
def tutor_profile():
    return render_template('tutoring/tutor_profile.html')

@tutoring.route('/tutor_session')
def tutor_session():
    return render_template('tutoring/tutor_session.html')