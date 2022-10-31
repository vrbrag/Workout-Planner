from distutils.command.build_scripts import first_line_re
from unittest import TestCase
from sqlalchemy import exc

from app import app
from models import db, User, Exercise, Workouts, ExerciseTracker

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gitfit_app_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class GetAPIExercisesTestCase(TestCase):
   """Test display and functionality of exercises"""

   def setUp(self):
      """Add sample exercise"""

      Exercise.query.delete()

   def tearDown(self):
      """Delete any transactions"""
      db.session.rollback()

   def test_show_API_exercises(self):

      with app.test_client() as client:
         resp = client.get('/exercises')
         
         self.assertEqual(resp.status_code, 302)
         
