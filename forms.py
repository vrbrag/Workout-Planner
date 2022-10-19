from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
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
   
class TrackWorkoutForm(FlaskForm):
   """Form to create workout"""

   name = StringField('Workout Name', validators=[DataRequired()])
   exercise = StringField('Exercise', validators=[DataRequired()])
   reps = IntegerField('Reps', validators=[Optional()])
   weight = IntegerField('Weight', validators=[Optional()])

class CreateWorkout(FlaskForm):

   name = StringField('Workout Name', validators=[DataRequired()])
   