from flask import render_template, request, Blueprint

from flask import Blueprint

courses = Blueprint('courses', __name__, template_folder='templates')