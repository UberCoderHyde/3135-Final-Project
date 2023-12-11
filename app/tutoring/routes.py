from .forms import CreateTutoringSessionForm, EditTutorProfileForm, EnrollmentForm
from flask_login import current_user, login_required
from app.models import Course, Enrollment, TutoringSession, User
from flask import flash, redirect, render_template, request, Blueprint, url_for
from app.extensions import db
from flask import Blueprint
from datetime import datetime

tutoring = Blueprint('tutoring', __name__, template_folder='templates', url_prefix="/tutoring")

@tutoring.route('/list_tutors')
def list_tutors():
    tutors = User.query.filter_by(is_tutor=True).all()
    courses_with_tutors = Course.query.all()
    return render_template('tutoring/list_tutors.html', tutors=tutors, courses_with_tutors=courses_with_tutors)

@tutoring.route('/tutor_profile/<int:tutor_id>')
def tutor_profile(tutor_id):
    tutor = User.query.get_or_404(tutor_id)
    sessions = TutoringSession.query.filter_by(tutor_id=tutor_id).all()
    return render_template('tutoring/tutor_profile.html', tutor=tutor, sessions=sessions)

@tutoring.route('/create_session', methods=['GET', 'POST'])
@login_required
def create_session():
    form = CreateTutoringSessionForm() 
    form.subject.choices = [(course.id, course.name) for course in current_user.courses]
    form.session_time.choices = form.generate_time_slots()
    print("Session Time Choices:")
    if form.validate_on_submit():
        session_time_str = form.session_time.data
        session_time = datetime.strptime(session_time_str, '%I:%M %p')
        new_session = TutoringSession(
            subject=form.subject.data,
            session_time=session_time,
            location=form.location.data,
            tutor_id=current_user.id,
        )
        db.session.add(new_session)
        db.session.commit()
        flash('Session created successfully', 'success')
        return redirect(url_for('tutoring.tutor_profile', tutor_id=current_user.id))
    return render_template('tutoring/create_session.html', form=form)

@tutoring.route('/tutor_session/<int:session_id>')
def tutor_session(session_id):
    session = TutoringSession.query.get_or_404(session_id)
    enrollments = Enrollment.query.filter_by(session_id=session_id).all()
    enroll_form = EnrollmentForm()  # Create an instance of EnrollmentForm
    return render_template('tutoring/tutor_session.html', session=session, enrollments=enrollments, enroll_form=enroll_form)

@tutoring.route('/enroll/<int:session_id>', methods=['POST'])
@login_required
def enroll(session_id):
    if not Enrollment.query.filter_by(session_id=session_id, user_id=current_user.id).first():
        enrollment = Enrollment(session_id=session_id, user_id=current_user.id, status='enrolled')
        db.session.add(enrollment)
        db.session.commit()
        flash('Enrolled in session successfully!', 'success')
    else:
        flash('You are already enrolled in this session.', 'info')
    return redirect(url_for('tutoring.tutor_session', session_id=session_id))

@tutoring.route('/edit_tutor_profile', methods=['GET', 'POST'])
@login_required
def edit_tutor_profile():
    form = EditTutorProfileForm()
    if form.validate_on_submit():
        current_user.description = form.description.data
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('tutoring.tutor_profile', tutor_id=current_user.id))
    
    elif request.method == 'GET':
        form.description.data = current_user.description
    return render_template('tutoring/edit_tutor_profile.html', form=form)