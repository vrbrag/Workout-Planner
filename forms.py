from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, widgets,IntegerField, SelectMultipleField, SelectField, SubmitField, FieldList, FormField
# from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, Length, Optional

class UserAddForm(FlaskForm):
   """Form for adding users"""

   username = StringField('Username', validators=[DataRequired()])
   email = StringField('Email', validators=[DataRequired()])
   password = PasswordField('Password', validators=[Length(min=6)])
   image_url = StringField('(optional) Image URL')

class LoginForm(FlaskForm):
   """Form for loggin in user"""

   username = StringField('Username', validators=[DataRequired()])
   password = PasswordField('Password', validators=[Length(min=6)])
   

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CreateWorkoutForm(FlaskForm):

   name = StringField('Name your workout...', validators=[DataRequired()])
   exercises = MultiCheckboxField('Exercises', choices=[], coerce=int)
   

class TrackWorkoutForm(FlaskForm):
   """Form to create workout"""

   sets = IntegerField('Sets', validators=[Optional()])
   reps = IntegerField('Reps', validators=[Optional()])
   unit_rep = SelectField('Unit', choices=['Reps', 'Max Reps', 'Til Failure', 'Miles', 'Minutes', 'Seconds'])
   weight = IntegerField('Weight', validators=[Optional()])
   unit_weight = SelectField('Unit', choices=['lbs', 'bodyweight', 'miles per hour'])
   notes = TextAreaField('Notes', validators=[Optional()])  