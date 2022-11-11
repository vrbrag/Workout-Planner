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
        default="/static/images/default-pic.png",)

   workouts = db.relationship(
       'Workouts',)
       
   exercises = db.relationship(
       'Exercise',)

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
      db.Integer, primary_key=True)

   name = db.Column(
      db.Text, nullable=False)

   description = db.Column(
      db.Text)

   dataID = db.Column(
         db.Integer)

   user_id = db.Column(
      db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))



class Workouts(db.Model):
   """Workouts,
   Some with same name and day, but unique ID's
   """

   __tablename__="workout"

   id = db.Column(
      db.Integer, primary_key=True)

   name = db.Column(
      db.Text, nullable=False)

   exerciseIDs = db.Column(
      db.String)
     
   user_id = db.Column(
      db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

   timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow())
   
   # exercise = db.relationship('Exercise')


class ExerciseTracker(db.Model):
   """Exercise Tracker,
   Log one exercise's reps and weight within a workout session
   """

   __tablename__="tracker"

   id = db.Column(
      db.Integer, primary_key=True)
   
   timestamp = db.Column(
      db.DateTime, nullable=False, default=datetime.utcnow())

   sets = db.Column(
      db.Integer)

   reps = db.Column(
      db.Integer)

   unit_rep = db.Column(
      db.String)

   weight = db.Column(
      db.Integer)
   
   unit_weight = db.Column(
      db.String)

   notes = db.Column(
      db.Text, default=None)

   exercise_id = db.Column(
      db.Integer, db.ForeignKey('exercise.id', ondelete='CASCADE'))
   
   user_id = db.Column(
      db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))




def connect_db(app):
   """Connect to database"""
   db.app = app
   db.init_app(app)