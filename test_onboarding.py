from distutils.command.build_scripts import first_line_re
from unittest import TestCase
from sqlalchemy import exc

from app import app
from models import db, User, Exercise, Workouts, ExerciseTracker

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gitfit_app_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
   """Tests for model Users"""

   def setUp(self):
      """Clean up any existing users"""
      User.query.delete()

      u1 = User.signup("test1", "email1@email.com", "password", None)
      uid1 = 1111
      u1.id = uid1
      db.session.commit()

      u1 = User.query.get(uid1)
      self.u1 = u1
      self.uid1 = uid1


   def tearDown(self):
      """Clean up any fouled transaction"""
      res = super().tearDown()
      db.session.rollback()
      return res


   def test_name(self):
      """Does basic model work?"""
      user = User(
         email='testuser@yahoo.com', 
         username='TestUser1', 
         password = 123456
      )
      db.session.add(user)
      db.session.commit()

      self.assertEqual(user.email, 'testuser@yahoo.com')
      self.assertEqual(user.username, 'TestUser1')
      self.assertEqual(user.image_url, '/static/images/default-pic.png')
      self.assertEqual(len(user.workouts), 0)

#####################################################################
# User Workouts Tests

   def test_user_workout(self):
      w1 = Workouts(name='Legs', exerciseIDs='[1,2]', user_id=self.uid1)
      self.u1.workouts.append(w1)
      db.session.commit()

      self.assertEqual(len(self.u1.workouts), 1)

#####################################################################
# Signup Tests 

   def test_user_signup(self):
      user_test = User.signup(email='test@yahoo.com', username='testUser', password='password', image_url=None)
      uid = 111
      user_test.id = uid
      db.session.commit()

      user = User.query.get(uid)
      self.assertIsNotNone(user_test)
      self.assertEqual(user.email, 'test@yahoo.com')
      self.assertEqual(user.username, 'testUser')
      self.assertTrue(user.password.startswith('$2b$'))
      self.assertEqual(user.image_url, '/static/images/default-pic.png')

   def test_invalid_email_signup(self):
      invalid = User.signup(
         email=None, 
         username='testUser', 
         password='password', 
         image_url=None)
      uid = 222
      invalid.id = uid
      with self.assertRaises(exc.IntegrityError) as context:
         db.session.commit()
   
   def test_invalid_username_signup(self):
      invalid = User.signup(
         email='test@yahoo.com', 
         username=None, 
         password='password', 
         image_url=None)
      uid = 222
      invalid.id = uid
      with self.assertRaises(exc.IntegrityError) as context:
         db.session.commit()

   def test_invalid_password_signup(self):
      with self.assertRaises(ValueError) as context:
         User.signup(
         email='test@yahoo.com', 
         username='testUser', 
         password='', 
         image_url=None)
         db.session.commit()

      with self.assertRaises(ValueError) as context:
         User.signup(
         email='test@yahoo.com', 
         username='testUser', 
         password=None, 
         image_url=None)
         db.session.commit()

#####################################################################
# Authentication Tests  

   def test_user_authentication(self):
      user_test = User.authenticate(self.u1.username, 'password')
      self.assertIsNotNone(user_test)
      self.assertEqual(user_test.id, self.uid1)

   def test_invalid_username_auth(self)  :
      self.assertFalse(User.authenticate('wrongusername', 'password'))

   def test_invalid_passworkd_auth(self):
      self.assertFalse(User.authenticate(self.u1.username, 'wrongpassword'))
