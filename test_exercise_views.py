from distutils.command.build_scripts import first_line_re
from unittest import TestCase
from sqlalchemy import exc

from app import app
from models import db, User, Exercise, Workouts, ExerciseTracker

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gitfit_app_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

# The 302 redirect, on the other hand, is only temporary. A good example of when to use a 302 status code is for localization and language purposes.
+
# For instance, if you visit a clothing website based in the United Kingdom but you are located in the United States. A 302 redirect would send you to the US version of the site to ensure the currency and other content are displayed correctly, according to your location.

class ExerciseViewsTestCase(TestCase):
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
         
