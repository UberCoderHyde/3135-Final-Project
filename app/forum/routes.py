from flask import render_template, request, redirect, url_for, flash, Blueprint
from .forms import ForumForm, ForumPostForm, CommentForm
from app.models import Forum, ForumPost, Comment, User
from flask_login import current_user, login_required
from app.extensions import db

forum = Blueprint('forum', __name__, template_folder='templates', url_prefix="/forum")

@forum.route('/forum')
def forum_home():
    forums = Forum.query.all()
    return render_template('forum/forum_home.html', forums=forums)


@forum.route('/forum_home/<int:forum_id>')
def forum_posts(forum_id):
    forum = Forum.query.get_or_404(forum_id)
    posts = ForumPost.query.filter_by(forum_id=forum.id).order_by(ForumPost.timestamp.desc()).all()
    return render_template('forum/forum_posts.html', forum=forum, posts=posts, forum_id=forum.id)

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
@forum.route('/new_forum', methods=['GET', 'POST'])
def new_forum():
    form = ForumForm()  # Use the appropriate form for creating a new forum
    if form.validate_on_submit():
        forum = Forum(title=form.name.data, description=form.description.data, user_id=current_user.id)
        db.session.add(forum)
        db.session.commit()
        flash('Forum created successfully!', 'success')
        return redirect(url_for('forum.forum_home'))

    return render_template('forum/new_forum.html', form=form)
@forum.route('/new_topic/<int:forum_id>', methods=['GET', 'POST'])
@login_required
def new_topic(forum_id):
    form = ForumPostForm()
    forum = Forum.query.get_or_404(forum_id)
    if form.validate_on_submit():
        post = ForumPost(title=form.title.data, body=form.body.data, user_id=current_user.id, forum_id=forum.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('forum.forum_posts', forum_id=forum.id))
    return render_template('forum/new_topic.html', form=form, forum=forum)

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
@forum.route('/delete_forum/<int:forum_id>', methods=['POST'])
def delete_forum(forum_id):
    forum = Forum.query.get_or_404(forum_id)

    # Check if the current user is the owner of the forum
    if current_user == forum.user:
        # Perform the deletion logic (You need to implement this part)
        # For example, you might delete associated posts, topics, etc.
        # Then delete the forum itself
        db.session.delete(forum)
        db.session.commit()

        flash('Forum deleted successfully', 'success')
    else:
        flash('You do not have permission to delete this forum', 'danger')

    return redirect(url_for('forum.forum_home')) 