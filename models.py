"""SQLAlchemy models for Fitness App"""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()



class User(db.Model):
   """User in the system"""

   __tablename__="users"

   id = db.Column(
        db.Integer, primary_key=True)

   email = db.Column(
      db.Text, nullable=False, unique=True)

   username = db.Column(
      db.Text, nullable=False, unique=True)

   password = db.Column(
      db.Text, nullable=False)

   image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

   def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

   @classmethod
   def signup(cls, username, email, password, image_url):
      """Sign up user.

      Hashes password and adds user to system.
      """

      hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

      user = User(
         username=username,
         email=email,
         password=hashed_pwd,
         image_url=image_url
      )

      db.session.add(user)
      return user

   @classmethod
   def authenticate(cls, username, password):
      """Find user with `username` and `password`.

      This is a class method (call it on the class, not an individual user.)
      It searches for a user whose password hash matches this password
      and, if it finds such a user, returns that user object.

      If can't find matching user (or if password is wrong), returns False.
      """

      user = cls.query.filter_by(username=username).first()

      if user:
         is_auth = bcrypt.check_password_hash(user.password, password)
         if is_auth:
               return user

      return False




class Exercise(db.Model):
   """Exercises"""

   __tablename__="exercise"

   id = db.Column(
      db.Integer, primary_key=True
   )

   exercise_name = db.Column(
      db.Text, nullable=False 
   )

   description = db.Column(
      db.Text
   )

   muscle = db.Column(
      db.Text
   )

   equipment = db.Column(
      db.Text, nullable=False
   )

   variation = db.Column(
      db.Text
   )

   exercise_category = db.Column(
      db.Text
   )

   images = db.Column(
        db.Text,
      #   default="/static/images/default-pic.png",
    )



class ExerciseRecord(db.Model):
   """Exercise record,
   Log one exercise's reps and weight within a workout session
   """

   __tablename__="record"

   id = db.Column(
      db.Integer, primary_key=True)

   reps = db.Column(
      db.Integer)

   weight = db.Column(
      db.Integer)

   workout_id = db.Column(
      db.Integer, db.ForeignKey('workout.id', ondelete='CASCADE'))

   exercise_id = db.Column(
      db.Integer, db.ForeignKey('exercise.id', ondelete='CASCADE'))
   
   notes = db.Column(
      db.Text)



class WorkoutSession(db.Model):
   """Workout session == One gym session
   """

   __tablename__="workout"

   id = db.Column(
      db.Integer, primary_key=True)

   name = db.Column(
      db.Text, nullable=False
   )

   date = db.Column(
      db.DateTime, nullable=False, default=datetime.utcnow())

   record_id = db.Column(
      db.Integer, db.ForeignKey('record.id', ondelete='CASCADE')
   )
   
   exercise_id = db.Column(
      db.Integer, db.ForeignKey('exercise.id', ondelete='CASCADE')
   )
      
   user_id = db.Column(
      db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

   user = db.relationship('User')


def connect_db(app):
   """Connect to database"""
   db.app = app
   db.init_app(app)