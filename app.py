import os
import requests
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify, json, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, CreateWorkoutForm, TrackWorkoutForm, FieldList, FormField
from models import db, connect_db, User, Exercise, ExerciseTracker, Workouts


CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.debug = True
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

# FLASK_APP=app.py FLASK_DEBUG=1 TEMPLATES_AUTO_RELOAD=1 flask run


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
# Search/Show/Save Exercise Info 
# -------------------------------------------------
@app.route('/exercises')
def show_all_exercises():
    """Show all exercises
    - search exercises by name
    """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user_exercises = curr_user_exercises(g.user)
    myExercises = [(exercises.dataID) for exercises in user_exercises]

    resp = requests.get(f"{BASE_URL}/exercise", params={'language':2, 'limit':232})
    data_exercises = resp.json()['results']

    return render_template('search_exercises.html', data_exercises=data_exercises, myExercises=myExercises)


@app.route('/exercise/<int:exercise_id>', methods=["GET"])
def show_exercise_info(exercise_id):
    """Show details of exercise"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
   
    res = get_API_exercise(exercise_id)  

    user_exercises = curr_user_exercises(g.user)
    myExercises = [(exercises.dataID) for exercises in user_exercises]
    return render_template('show_exercise.html', res=res, myExercises=myExercises)


@app.route('/exercise/<int:exercise_id>/save', methods=["GET"])
def save_exercise(exercise_id):
    """Save exercise"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    res = get_API_exercise(exercise_id)       
    new_exercise = Exercise(
        name = res['name'],
        description = res['description'],
        dataID = res['id'],
        user_id = session[CURR_USER_KEY]
    )
    db.session.add(new_exercise)
    db.session.commit()
    flash(f"'{res['name']}' exercise saved", "info")
    return redirect('/exercises')

def get_API_exercise(id):
    """Get one api exercise"""
    resp = requests.get(f"{BASE_URL}/exerciseinfo", params={'language':2, 'limit':386})
    data = resp.json()['results']
  
    res = None
    for exercise in data:
        if exercise['id'] == id:
            res = exercise
    return res
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
        # print(workouts)
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

    user_exercises = curr_user_exercises(g.user)
    form = CreateWorkoutForm()
    form.exercises.choices = [(exercises.id, exercises.name) for exercises in user_exercises]

    if request.method == "POST" and form.validate_on_submit():
        print(form.exercises.data) # list
        json_exerciseIDs = string_exerciseIDs(form.exercises.data)
        new_workout = Workouts(
                    name = form.name.data,
                    exerciseIDs = json_exerciseIDs,
                    user_id = session[CURR_USER_KEY] # user id
                )
        db.session.add(new_workout)
        db.session.commit()
        flash (f"Success! Created new workout, '{form.name.data}'.", 'success')
        return redirect('/')
    return render_template('workout/new.html', form=form )

def string_exerciseIDs(exerciseIDs):
    """Function to stringify list of selected exercise IDs from new workout form"""
    selected = []
    for exerciseID in exerciseIDs:
        selected.append(exerciseID)
    json_exerciseIDs = json.dumps(selected, separators=(',', ':'))
    return json_exerciseIDs

# -------------------------------------------------
# Edit workout 
# -------------------------------------------------
@app.route('/workout/<int:workout_id>/edit', methods=["GET", "POST"])
def edit_workout(workout_id):
    """Edit workout"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    workout = Workouts.query.get_or_404(workout_id)
    
    user_exercises = curr_user_exercises(g.user)
    form = CreateWorkoutForm(obj=workout)
    form.exercises.choices = [(exercises.id, exercises.name) for exercises in user_exercises]
    # form.exercises.data = (parsedExerciseIDs)

    if request.method == "POST" and form.validate_on_submit():
        workout.name = form.name.data
        workout.exerciseIDs = string_exerciseIDs(form.exercises.data)
        db.session.commit()

        flash (f"'{form.name.data}' updated!", 'success')
        return redirect(f'/workout/{workout.id}')
    return render_template('workout/update.html', workout=workout, form=form)

# -------------------------------------------------
# Delete workout 
# -------------------------------------------------
@app.route('/workout/<int:workout_id>/delete', methods=["GET", "POST"])
def delete_workout(workout_id):
    """Delete workout 
    Render to homepage"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    workout = Workouts.query.get_or_404(workout_id)
    if workout.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(workout)
    db.session.commit()
    return redirect('/')

# -------------------------------------------------
# Show workout (details of each exercise)
# -------------------------------------------------
@app.route('/workout/<int:workout_id>')
def show_workout(workout_id):
    """Show workout info"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    workout = Workouts.query.get_or_404(workout_id)     
    my_exercises = get_workout_exercises(workout.exerciseIDs)
     
    return render_template('workout/show.html', workout=workout, my_exercises=my_exercises)

def get_workout_exercises(ids):
    parsedExerciseIDs = json.loads(ids)
    workout_exercises = (Exercise
                .query
                .filter(Exercise.id.in_(parsedExerciseIDs))
                .all())
    return workout_exercises

def get_API_data(dataIDs):
    """Call API for full exercise data
    - parameter: dict of exercise id/dataIDs"""
    resp = requests.get(f"{BASE_URL}/exerciseinfo", params={'language':2, 'limit':386})
    data = resp.json()['results']
    
    res = []
    for exercise in data:
        if exercise['id'] in dataIDs:
            res.append(exercise)
    return res 

# -------------------------------------------------
# Get Exercise Varations
# -------------------------------------------------
@app.route('/exercise/variations/<variations>')
def show_variations(variations):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    parsedExerciseIDs = json.loads(variations)
    exercises = get_API_data(parsedExerciseIDs)
    return render_template('variations.html', exercises=exercises)

# -------------------------------------------------
# Track Workout
# -------------------------------------------------
@app.route('/track/<int:workout_id>/<int:exercise_id>', methods=['GET','POST'])
def track_workout(workout_id, exercise_id):

    exercise = Exercise.query.get_or_404(exercise_id)

    form = TrackWorkoutForm()
    if request.method == "POST" and form.validate_on_submit():
        track = ExerciseTracker(
            reps = request.form['reps'],
            sets = request.form['sets'],
            unit_rep = form.unit_rep.data,
            weight = form.weight.data,
            unit_weight = form.unit_weight.data,
            notes = form.notes.data or None,
            exercise_id = exercise_id,
            user_id = session[CURR_USER_KEY]
        ) 
        db.session.add(track)  
        db.session.commit()
        flash(f"'{exercise.name}' - new log saved!", "success")
        return redirect(url_for('show_workout', workout_id=workout_id))
    
    return render_template ('track_workout.html', exercise=exercise, form=form)


# _________________________________________________
# *********** Functions **********
# _________________________________________________
def curr_user_exercises(user):
    """Filter for curr_user's exercises in Exercise"""
    print(user)
    exercise_ids = [exercise.id for exercise in user.exercises] + [user.id]
    exercises = (Exercise
                    .query
                    .filter(Exercise.user_id.in_(exercise_ids))
                    .all()
                    )
    return exercises