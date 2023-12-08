from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Length

class EditProfileForm(FlaskForm):
    description = TextAreaField('Description', validators=[Length(max=1000)])
    submit = SubmitField('Update Profile')