from distutils.command.build_scripts import first_line_re
from unittest import TestCase
from sqlalchemy import exc

from app import app, json, CURR_USER_KEY, get_API_exercise
from models import db, User, Exercise, Workouts, ExerciseTracker

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gitfit_app_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

# The 302 redirect, on the other hand, is only temporary. A good example of when to use a 302 status code is for localization and language purposes.

# For instance, if you visit a clothing website based in the United Kingdom but you are located in the United States. A 302 redirect would send you to the US version of the site to ensure the currency and other content are displayed correctly, according to your location.

class ExerciseViewsTestCase(TestCase):
   """Test display and functionality of exercises"""

   def setUp(self):
      """Add sample exercise"""


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

      # Add 1 sample Exercise *saved to db* 
      ex1 = Exercise(
         name ='2 Handed Kettlebell Swing',
         description = '<p>Two Handed Russian Style Kettlebell swing</p>',
         dataID = 345,
         user_id = self.testuser_id
      )
      db.session.add(ex1)
      db.session.commit()

      self.ex1_id = ex1.id

   def tearDown(self):
      """Delete any transactions"""
      db.session.rollback()

   def test_search_API_exercises(self):

      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id
         resp = client.get('/exercises')
         
         
         self.assertEqual(resp.status_code, 200)
         self.assertIn('2 Handed Kettlebell Swing', str(resp.data))

   def test_show_API_exercise_detail(self):

      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id
         resp = client.get('/exercise/345')
         html = resp.get_data(as_text=True)

         self.assertEqual(resp.status_code, 200)
         self.assertIn('<h6>Description</h6>', str(resp.data))
         self.assertIn('<h6>Equipment</h6>', str(resp.data))
         self.assertIn('2 Handed Kettlebell Swing', str(resp.data))
         
 
   def test_get_API_exercise(self):
      """Test function 
      - request to api 
      - return dictionary of exercise data"""
      dataID = 345
      exercise_dict = get_API_exercise(dataID)
      print(exercise_dict)
      self.assertEqual(type(exercise_dict), dict)
      self.assertEqual(exercise_dict['name'], '2 Handed Kettlebell Swing')
      self.assertEqual(exercise_dict['equipment'][0]['name'], 'Kettlebell')
         


         
