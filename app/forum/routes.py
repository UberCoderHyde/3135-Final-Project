from flask import render_template, request, redirect, url_for, flash, Blueprint
from .forms import ForumPostForm, CommentForm
from app.models import ForumPost, Comment, User
from flask_login import current_user, login_required
from app.extensions import db
forum = Blueprint('forum', __name__, template_folder='templates',url_prefix="/forum")
@forum.route('/forum')
def forum_home():
    posts = ForumPost.query.order_by(ForumPost.timestamp.desc()).all()
    return render_template('forum/forum.html', posts=posts)

@forum.route('/forum_topic/<int:post_id>', methods=['GET', 'POST'])
def forum_topic(post_id):
    post = ForumPost.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.timestamp.asc()).all()
    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(body=form.body.data, user_id=current_user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('forum.forum_topic', post_id=post_id))
    return render_template('forum/forum_topic.html', post=post, comments=comments, form=form)

@forum.route('/new_topic', methods=['GET', 'POST'])
@login_required
def new_topic():
    form = ForumPostForm()
    if form.validate_on_submit():
        post = ForumPost(title=form.title.data, body=form.body.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('forum.forum_home'))
    return render_template('forum/new_topic.html', form=form)

@forum.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    
    # Check if the current user is allowed to delete the post
    if post.author != current_user:  # Adjust as needed for your authorization logic
        flash('You do not have permission to delete this post.', 'danger')
        return redirect(url_for('forum.forum_topic', post_id=post.id))

    # First, delete comments associated with the post
    Comment.query.filter_by(post_id=post.id).delete()

    # Then, delete the post itself
    db.session.delete(post)
    db.session.commit()

    flash('The post and all associated comments have been deleted.', 'success')
    return redirect(url_for('forum.forum_home'))