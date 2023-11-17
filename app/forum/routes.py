from flask import render_template, request, Blueprint

from flask import Blueprint

forum = Blueprint('forum', __name__, template_folder='templates',url_prefix="/forum")
@forum.route('/forum_topic')
def forum_topic():
    return render_template('forum/forum_topic.html')
@forum.route('/forum')
def forum():
    return render_template('forum/forum.html')
@forum.route('/new_topic')
def new_topic():
    return render_template('forum/new_topic.html')