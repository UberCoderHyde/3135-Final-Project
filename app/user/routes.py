from flask import render_template, request, Blueprint

from flask import Blueprint

user = Blueprint('user', __name__, template_folder='templates')