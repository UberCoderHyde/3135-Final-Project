from flask import render_template, request, Blueprint

from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates')