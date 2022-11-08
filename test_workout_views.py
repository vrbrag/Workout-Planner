from distutils.command.build_scripts import first_line_re
from unittest import TestCase, skip
from sqlalchemy import exc
 
from app import app, json, CURR_USER_KEY, get_workout_exercises, string_exerciseIDs, get_API_data
from models import db, User, Exercise, Workouts, ExerciseTracker
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gitfit_app_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
 
# python -m unittest test_workout_views.py
 
db.drop_all()
db.create_all()
 
class WorkoutViewsTestCase(TestCase):
 
   def setUp(self):
      db.drop_all()
      db.create_all()

      # User.query.delete()
      # Workouts.query.delete()
      # Exercise.query.delete()

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
      
 
   def tearDown(self):
      """Delete any transactions"""
      res = super().tearDown()
      db.session.rollback()
      return res
   
#### Add new workout #############
   # @skip ('skip for now')
   def test_new_workout_form(self):
      """Test show new workout form"""
      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id
         
         resp = client.get('/workout/new')
         html = resp.get_data(as_text=True) 
         
         self.assertEqual(resp.status_code, 200)
         self.assertIn('class="form-control" id="exercises"', html)

         exercise = [exercise for exercise in Exercise.query.all()]
         self.assertIn(exercise[1].name, 'Front Squats')

   # @skip ('skip for now')
   def test_function_string_exerciseIDs(self):
      """Test function: string_exerciseIDs"""
      form_exercises_data = [1,2,3]
      self.assertEqual(string_exerciseIDs(form_exercises_data), '[1,2,3]')

   # @skip ('skip for now')
   def test_add_new_workout(self):
      """Test 'POST' new workout form
      - Redirect to homepage that should show new workout name"""
      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id
         
         d = {"name": "Workout 1", "exerciseIDs":"[1,2,3]", "user_id": sess[CURR_USER_KEY]}
         resp = client.post('/workout/new', data=d, follow_redirects=True)
         html = resp.get_data(as_text=True) 

         self.assertEqual(resp.status_code, 200)
         self.assertIn("My Workouts", html)  # title of homepage
         self.assertIn('Workout 1', html)    # title of new workout


#### Delete Workout #############
   # @skip ('skip for now')
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
         w = Workouts.query.get(1)
         resp = client.post(f'/workout/{w.id}/delete')
   
         self.assertEqual(resp.status_code, 302)
         w = Workouts.query.get(1)
         self.assertIsNone(w)

   # @skip ('skip for now')
   def test_invalid_workout_delete(self):
      u = User.signup(username="unauthorized-user",
                        email="testtest@test.com",
                        password="password",
                        image_url=None)
      u.id = 76543

      w = Workouts(
         id=123,
         name='Legs',
         exerciseIDs='[1,2,3]',
         user_id=self.testuser.id
      )
      db.session.add_all([u,w])
      db.session.commit()
 
      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = 76543

         resp = client.post('/workout/123/delete', follow_redirects=True) 

         self.assertEqual(resp.status_code, 200)
         self.assertIn("Access unauthorized", str(resp.data))

         w = Workouts.query.get(123)
         self.assertIsNotNone(w)



#### Show User Workout #############
   # @skip ('skip for now')
   def test_workout_show(self):
      """Test show workout"""
      w = Workouts(
         id=1,
         name='Workout 1',
         exerciseIDs='[1,2]',
         user_id=self.testuser.id
      )
      db.session.add(w)
      db.session.commit()
   
      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id
         
         w = Workouts.query.get(1)
         resp = client.get(f'/workout/{w.id}')
         html = resp.get_data(as_text=True)
   
         self.assertEqual(resp.status_code, 200)
         # Workout name 
         self.assertIn(w.name, str(resp.data))
         # Exercise 2 name
         self.assertIn('Front Squats', str(resp.data))
         
   
   # @skip ('skip for now')
   def test_function_get_workout_exercises(self):
      """Test function to get workout's exercises
      - Convert string of ids to list
      - Return list of exercise models found in database"""
      ids_string = '[1,2,3]'
      exercises = get_workout_exercises(ids_string)
      self.assertEqual(type(exercises), list)
      # 'exercises' should equal models found in Exercise db (via setUp function)
      db_exercises = Exercise.query.all()
      self.assertEqual(exercises, db_exercises)
      

   # @skip ('skip for now')
   def test_invalid_workouts_show(self):
      with app.test_client() as client:
         with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id
         
         resp = client.get('/workout/22')

         self.assertEqual(resp.status_code, 404)