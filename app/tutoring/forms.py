from flask_wtf import FlaskForm
from wtforms import DateField, StringField, DateTimeField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Length

class CreateTutoringSessionForm(FlaskForm):
    subject = SelectField('Subject',choices=[], coerce=int, validators=[DataRequired()])
    session_date = DateField('Session Date', format='%Y-%m-%d', validators=[DataRequired()])
    session_time = SelectField('Session Time', coerce=str, validators=[DataRequired()])
    location_type = SelectField('Location Type', choices=[('in_person', 'In-Person'), ('online', 'Online')], validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])    
    submit = SubmitField('Create Session')

    def __init__(self, *args, **kwargs):
        super(CreateTutoringSessionForm, self).__init__(*args, **kwargs)
        self.session_time.choices = self.generate_time_slots()

    @staticmethod
    def generate_time_slots():
        time_slots = []
        for hour in range(7, 22):  # From 7 AM to 9 PM
            for minute in [0, 30]:
                # Convert to 12-hour format
                hour_12 = hour if 1 <= hour <= 12 else hour - 12
                meridiem = "AM" if hour < 12 else "PM"
                time_slots.append(f'{hour_12:02d}:{minute:02d} {meridiem}')
        return time_slots

class EnrollmentForm(FlaskForm):
    submit = SubmitField('Enroll in Session')
class EnrollmentForm(FlaskForm):
    submit = SubmitField('Enroll in Session')

class EditTutorProfileForm(FlaskForm):
    description = TextAreaField('Description', validators=[Length(max=1000)])
    submit = SubmitField('Update Profile')