import os
import requests
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify, json
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, TrackWorkoutForm, CreateWorkoutForm
from models import db, connect_db, User, Exercise, ExerciseTracker, Workouts


CURR_USER_KEY = "curr_user"

app = Flask(__name__)

BASE_URL = 'https://wger.de/api/v2/'
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///gitfit_app'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()




# _________________________________________________
# **********/ SignUp / Login /Logout **************
# _________________________________________________
# -------------------------------------------------
# User SignUp/Login/Logout
# -------------------------------------------------
@app.before_request
def add_user_to_g():
    """If logged in, add curr user to Flask global"""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user"""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Log out user"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def register_user_form():
    """User sign up 
    - Create new user and add to DB. Redirect to homepage
    - If invalid form submittal, re-display form with flash message
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)
        
        do_login(user)

        return redirect('/')
    
    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle login of user"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data, 
            form.password.data
        )

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect('/')

        flash("Invalid credentials.", "danger")

    else:
        return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash('You have been logged out', 'info')
    return redirect('/login')
# _________________________________________________
# *****************/ Exercises Tab ****************
# _________________________________________________
# -------------------------------------------------
# Search EXERCISES & Exercise INFO
# -------------------------------------------------
@app.route('/exercises')
def show_all_exercises():
    """Show all exercises
    - search exercises by name
    """
    myExercises = [exercises.serialize() for exercises in Exercise.query.all()]

    resp = requests.get(f"{BASE_URL}/exercise", params={'language':2, 'limit':232})
    data_exercises = resp.json()['results']

    return render_template('search_exercises.html', data_exercises=data_exercises, myExercises=myExercises)


@app.route('/exercise/<int:exercise_id>', methods=["GET"])
def show_exercise_info(exercise_id):
    """Show details of exercise"""

    resp = requests.get(f"{BASE_URL}/exercise", params={'language':2, 'limit':232})
    data = resp.json()['results']
  
    res = None
    for exercise in data:
        if exercise['id'] == exercise_id:
            res = exercise
            
            new_exercise = Exercise(
                name = res['name'],
                description = res['description'],
                category = res['category'],
                equipment = res['equipment'],
                variations = res['variations'],
                dataID = res['id']
            )
            db.session.add(new_exercise)
            db.session.commit()
    
    return render_template('show_exercise.html', res=res)

# _________________________________________________
# ***********/ Homepage / My Workout Tab **********
# _________________________________________________
# -------------------------------------------------
@app.route("/")
def homepage():
    """Show homepage:
    - logged in user : 
    - anon user : login / register
    """

    if g.user:
        workout_ids = [workout.id for workout in g.user.workouts] + [g.user.id]
        # print(g.user)
        workouts = (Workouts
                    .query
                    .filter(Workouts.user_id.in_(workout_ids))
                    .order_by(Workouts.timestamp.desc())
                    .all()
                    )
        return render_template('users/home.html', workouts=workouts, workout_ids=workout_ids)
    else:
        return render_template('home-anon.html')

# -------------------------------------------------
# Create new workout 
# -------------------------------------------------
@app.route('/workout/new', methods=['GET','POST'])
def create_workout():
    """Show new workout form
    - get list of all saved exercises for logged in user
    - submit new workout """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = CreateWorkoutForm()
    form.exercises.choices = [(exercises.id, exercises.name) for exercises in Exercise.query.all()]

    if request.method == "POST" and form.validate_on_submit():
        createWorkout(form.exercises.data, form.name.data)
        return redirect('/')
    return render_template('workout/new.html', form=form )

def createWorkout(exerciseIDs, workoutName):
    """Function to create/commit new workout session"""
    selected = []
    for exerciseID in exerciseIDs:
        selected.append(exerciseID)
    json_workoutlist = json.dumps(selected, separators=(',', ':'))
    workout = Workouts(
                    name = workoutName,
                    exerciseIDs = json_workoutlist,
                    user_id = session[CURR_USER_KEY] #need user id
                )
    db.session.add(workout)
    db.session.commit()

# -------------------------------------------------
# Show workout (details of each exercise)
# -------------------------------------------------
@app.route('/workout/<int:workout_id>')
def show_workout(workout_id):
    """Show workout info"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    workout = Workouts.query.get_or_404(workout_id) # get workout's data
    api_IDs = getExerciseDataIDs(workout)    # parse & get list of exercise.dataIDs
    results = getAPIData(api_IDs)  # plug in API ids to find exercise data
  
    return render_template('workout/show.html', workout=workout, api_IDs=api_IDs, results=results)

def getExerciseDataIDs(workout):
    """Parse workout.exerciseIDs
    And filter for workout.exerciseIDs in Exercise db """
    parsedExerciseIDs = json.loads(workout.exerciseIDs)
    exercises = (Exercise
                .query
                .filter(Exercise.id.in_(parsedExerciseIDs))
                .all())
    api_IDs = list([exercise.dataID for exercise in exercises])
    return api_IDs  # return list of dataID's

def getAPIData(ids):
    """Call API for full exercise results
    - parameter: list of API data ids"""
    resp = requests.get(f"{BASE_URL}/exerciseinfo", params={'language':2, 'limit':232})
    data = resp.json()['results']

    res = []
    for exercise in data:
        if exercise['id'] in ids:
            res.append(exercise)
    return res  # return list of API exercise data

