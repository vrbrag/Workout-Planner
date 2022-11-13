from distutils.command.build_scripts import first_line_re
from unittest import TestCase, skip
from sqlalchemy import exc
 
from app import app, CURR_USER_KEY
from models import db, User, Exercise, Workouts, ExerciseTracker
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gitfit_app_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
 
# python -m unittest test_track_views.py
 
db.drop_all()
db.create_all()
 
class TrackerViewsTestCase(TestCase):
 
   def setUp(self):
      db.drop_all()
      db.create_all()

      # Add 1 sample User
      self.testuser = User.signup(
         username='testuser',
         email='test@test.com',
         password='password',
         image_url=None
      )
      self.testuser_id = 111
      self.testuser.id = self.testuser_id
      db.session.commit()

      # Add 3 sample Exercises
      self.ex1 = Exercise(
         name ='2 Handed Kettlebell Swing',
         description = '<p>Two Handed Russian Style Kettlebell swing</p>',
         dataID = 345,
         user_id = self.testuser_id
      )
      self.ex2 = Exercise(
         name ='Front Squats',
         description = '<p>Squats</p>',
         dataID = 191,
         user_id = self.testuser_id
      )
      self.ex3 = Exercise(
         name ='Good Mornings',
         description = '',
         dataID = 116,
         user_id = self.testuser_id
      )
 
      self.ex1_id = 1
      self.ex2_id = 2
      self.ex3_id = 3
   
      self.ex1.id = self.ex1_id
      self.ex2.id = self.ex2_id
      self.ex3.id = self.ex3_id
      db.session.add_all([self.ex1, self.ex2, self.ex3])
      db.session.commit()
      
      # Add 1 Workout, consists of exercises [1,2]
      self.w1 = Workouts(
         name = 'Workout 1',
         exerciseIDs = '[1,2]',
         user_id = self.testuser_id
      )

      self.w1_id = 1
      self.w1.id = self.w1_id
      db.session.add(self.w1)
      db.session.commit()
 
   def tearDown(self):
      """Delete any transactions"""
      res = super().tearDown()
      db.session.rollback()
      return res

#### Add new exercise log ###################
   # @skip ('skip for now')
   def test_show_new_log_form(self):
      """Test log form"""
      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id
         
         resp = client.get(f'/track/{self.w1_id}/{self.ex1_id}')
         html = resp.get_data(as_text=True) 

         self.assertEqual(resp.status_code, 200)
         self.assertIn('Sets', html)
         self.assertIn('Reps', html)

   # @skip ('skip for now')
   def test_add_new_log(self):
      """Test add log """
      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id
         
         d = {'sets':1, 'reps':2, 'unit_rep':'Reps', 'weight':3, 'unit_weight':'lbs', 'exercise_id':1, 'user_id':sess[CURR_USER_KEY]}
         resp = client.get(f'/track/{self.w1_id}/{self.ex1_id}', data=d, follow_redirects=True)

         self.assertEqual(resp.status_code, 200)

#### Show exercise log ###################
   # @skip ('skip for now')
   def show_exercise_log(self):
      """Test saving new exercise log"""

      t1 = ExerciseTracker(
         sets = 1,
         reps = 2,
         unit_rep = 'Reps',
         weight = 3,
         unit_weight = 'lbs',
         notes = 'Too easy!',
         exercise_id = self.ex1_id,
         user_id = self.testuser_id
      )
      db.session.add(t1)
      db.session.commit()

      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id
         
         resp = client.get(f'/workout/{self.w1_id}')

         self.assertEqual(resp.status_code, 200)
         self.assertIn('Too easy!', str(resp.data))

   # @skip ('skip for now')
   def test_invalid_user_show_exercise_log(self):
      """Invalid user cannot see other user's logs"""
      u = User.signup(username="unauthorized-user",
                        email="testtest@test.com",
                        password="password",
                        image_url=None)
      u.id = 76543

      t1 = ExerciseTracker(
         sets = 1,
         reps = 2,
         unit_rep = 'Reps',
         weight = 3,
         unit_weight = 'lbs',
         notes = 'Too easy!',
         exercise_id = self.ex1_id,
         user_id = self.testuser_id
      )
      db.session.add_all([u, t1])
      db.session.commit()

      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = 76543
         
         resp = client.get(f'/workout/{self.w1_id}')
         
         self.assertEqual(resp.status_code, 200)
         self.assertNotIn('Too easy!', str(resp.data))
         self.assertIsNotNone(t1)