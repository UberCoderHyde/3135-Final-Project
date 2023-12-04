from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CreateCourseForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Course Description', validators=[DataRequired()])
    submit = SubmitField('Create Course')
