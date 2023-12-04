from flask import render_template, request, Blueprint
from app.models import User, Course

from flask import Blueprint,jsonify

main = Blueprint('main', __name__, template_folder='templates')

# Route for the home page
@main.route('/')
@main.route('/home')
def index():
    return render_template('main/home.html')
# Route for the about page
@main.route('/about')
def about():
    return render_template('main/about.html')

# Route for the contact page
@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Here you might handle form submission (e.g., sending an email)
        pass
    return render_template('main/contact.html')

# Additional routes can be added in a similar manner
@main.route('/search-results')
def search_results():
    query = request.args.get('query', '').strip()

    # Search for users, courses, and tutors based on the query
    users = User.query.filter(User.username.ilike(f'%{query}%')).all()
    courses = Course.query.filter(Course.name.ilike(f'%{query}%')).all()

    # You may need to adjust the search criteria for tutors based on your requirements
    tutors = User.query.filter(User.is_tutor).filter(User.username.ilike(f'%{query}%')).all()

    return render_template('main/search_results.html', query=query, users=users, courses=courses, tutors=tutors)
@main.route('/search-suggestions')
def search_suggestions():
    query = request.args.get('query', '').strip()

    # Fetch user, course, and tutor suggestions based on the query
    user_suggestions = [user.username for user in User.query.filter(User.username.ilike(f'%{query}%')).limit(5)]
    course_suggestions = [course.name for course in Course.query.filter(Course.name.ilike(f'%{query}%')).limit(5)]
    tutor_suggestions = [tutor.username for tutor in User.query.filter(User.is_tutor).filter(User.username.ilike(f'%{query}%')).limit(5)]

    suggestions = user_suggestions + course_suggestions + tutor_suggestions
    return jsonify(suggestions)