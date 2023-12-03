from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length

class TutoringSessionForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired(), Length(max=100)])
    session_time = DateTimeField('Session Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=120)])
    submit = SubmitField('Create Session')

class EnrollmentForm(FlaskForm):
    submit = SubmitField('Enroll in Session')
