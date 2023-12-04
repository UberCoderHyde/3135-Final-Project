from flask import render_template, request, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import CreateCourseForm
from app.models import User, Course, TutoringSession
from app.extensions import db
courses = Blueprint('courses', __name__, template_folder='templates', url_prefix='/courses')

@courses.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    form = CreateCourseForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data, description=form.description.data, creator_id=current_user.id)
        course.tutors.append(current_user)  # Add the creator as a tutor
        db.session.add(course)
        db.session.commit()
        flash('Course created successfully!', 'success')
        return redirect(url_for('courses.list_courses'))
    return render_template('courses/add_course.html', form=form)

@courses.route('/join_course/<int:course_id>', methods=['POST'])
@login_required
def join_course(course_id):
    course = Course.query.get_or_404(course_id)
    if current_user not in course.tutors:
        course.tutors.append(current_user)
        db.session.commit()
        flash('You have joined the course as a tutor.', 'success')
    else:
        flash('You are already a tutor for this course.', 'info')
    return redirect(url_for('courses.course_detail', course_id=course_id))

@courses.route('/course_detail/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('courses/course_detail.html', course=course)

@courses.route('/list_courses')
def list_courses():
    courses = Course.query.all()
    return render_template('courses/list_courses.html', courses=courses)

@courses.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    # Check if current_user is one of the tutors for this course
    if current_user not in course.tutors:
        flash('You do not have permission to edit this course.', 'danger')
        return redirect(url_for('courses.course_detail', course_id=course_id))
    form = CreateCourseForm(obj=course)
    if form.validate_on_submit():
        course.name = form.name.data
        course.description = form.description.data
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('courses.course_detail', course_id=course.id))
    return render_template('courses/edit_course.html', form=form, course=course)
# In your courses blueprint file

@courses.route('/delete_course/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    if current_user.id != course.creator_id:
        flash("You do not have permission to delete this course.", "warning")
        return redirect(url_for('courses.course_detail', course_id=course_id))

    # If the current user is the creator, proceed with deletion
    db.session.delete(course)
    db.session.commit()
    flash("Course deleted successfully.", "success")
    return redirect(url_for('courses.list_courses'))
