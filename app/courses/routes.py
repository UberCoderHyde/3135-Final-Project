from flask import render_template, request, Blueprint

from flask import Blueprint

courses = Blueprint('courses', __name__, template_folder='templates', url_prefix = '/courses')
@courses.route('/add_course')
def add_course():
    return render_template('courses/add_course.html')

@courses.route('/course_detail')
def course_detail():
    return render_template('courses/course_detail.html')

@courses.route('/edit_course')
def edit_course():
    return render_template('courses/edit_course.html')

@courses.route('/list_courses')
def list_courses():
    return render_template('courses/list_courses.html')

