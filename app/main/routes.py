from flask import render_template, request, Blueprint

from flask import Blueprint

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
