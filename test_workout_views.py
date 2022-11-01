from distutils.command.build_scripts import first_line_re
from unittest import TestCase
from sqlalchemy import exc
 
from app import app, json, CURR_USER_KEY, get_exercise_DataIDs
from models import db, User, Exercise, Workouts, ExerciseTracker
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gitfit_app_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
 
# python -m unittest test_workout_views.py
 
db.drop_all()
db.create_all()
 
class WorkoutViews(TestCase):
 
   def setUp(self):
 
      User.query.delete()
      Workouts.query.delete()
      Exercise.query.delete()

      # Add sample User
      self.testuser = User.signup(
         username='testuser',
         email='test@test.com',
         password='password',
         image_url=None
      )
      self.testuser_id = 111
      self.testuser.id = self.testuser_id
      db.session.commit()

      # Add sample Exercises
      self.ex1 = Exercise(
         name ='2 Handed Kettlebell Swing',
         description = '<p>Two Handed Russian Style Kettlebell swing</p>',
         dataID = 345
      )
      self.ex2 = Exercise(
         name ='Front Squats',
         description = '<p>Squats</p>',
         dataID = 191
      )
      self.ex3 = Exercise(
         name ='Good Mornings',
         description = '',
         dataID = 116
      )
 
      self.ex1_id = 1
      self.ex2_id = 2
      self.ex3_id = 3
   
      self.ex1.id = self.ex1_id
      self.ex2.id = self.ex2_id
      self.ex3.id = self.ex3_id
      
      db.session.commit()
      
 
   def tearDown(self):
      """Delete any transactions"""
      res = super().tearDown()
      db.session.rollback()
      return res
   
   def add_workout(self):
 
      # self.assertEqual(self.ex1.name, '2 Handed Kettlebell Swing')
      # self.assertEqual(self.ex2.description, '<p>Squats</p>')
      # self.assertEqual(self.ex2.dataID, 116)
   
      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id
         resp = client.post('/workout/new', data={
            "name": 'Legs',
            "exerciseIDs":'[1,2,3]',
            "user_id" : sess[CURR_USER_KEY]})

         self.assertEqual(resp.status_code, 302)
         workout = Workouts.query.all()
         self.assertEqual(len(workout), 1)
 
   def test_workout_delete(self):
      w = Workouts(
         id=1,
         name='Legs',
         exerciseIDs='[1,2,3]',
         user_id=self.testuser.id
      )
      db.session.add(w)
      db.session.commit()
   
      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id
         resp = client.post('/workout/1/delete')
   
         self.assertEqual(resp.status_code, 302)
         w = Workouts.query.get(1)
         self.assertIsNone(w)
 
  # def test_workout_show(self):
 
  #    w = Workouts(
  #       id=1,
  #       name='Legs',
  #       exerciseIDs='[1,2,3]',
  #       user_id=self.testuser.id
  #    )
  #    db.session.add(w)
  #    db.session.commit()
 
  #    with app.test_client() as client:
 #       with client.session_transaction() as sess:
  #          sess[CURR_USER_KEY] = self.testuser.id
       
  #       w = Workouts.query.get(1)
  #       resp = client.post(f'/workout/{w.id}')
 
  #       self.assertEqual(resp.status_code, 200)
 
   def test_get_exercise_DataIDs(self):
      w = Workouts(
         id=1,
         name='Legs',
         exerciseIDs= '[1]',
         user_id=self.testuser.id
      )
      db.session.add(w)
      db.session.commit()
      
      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id
         workout = Workouts.query.get(1)
         resp = client.get(f'/exercise/{workout.id}')

         self.assertEqual(resp.status_code, 200)
         # workout exIDs == str of Exercise id
         self.assertEqual(workout.exerciseIDs, str([self.ex1_id])) 
      
         # return sample ex1.dataID = 345
         # self.assertEqual(get_exercise_DataIDs(workout), [345])