from flask import render_template, request, Blueprint

from flask import Blueprint

forum = Blueprint('forum', __name__, template_folder='templates')