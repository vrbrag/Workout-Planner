import os
import requests
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, TestTable, User, Exercise, ExerciseRecord, WorkoutPlan, WorkoutSession


CURR_USER_KEY = "curr_user"

app = Flask(__name__)

BASE_URL = 'https://wger.de/api/v2/'
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///fitness-app'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def homepage():

    return render_template('testbase.html')

# ________________________________________
# ----------------------------------------
# ALL EXERCISES & Exercise INFO
# ----------------------------------------
@app.route("/exercises")
def show_all_exercises():
    resp = requests.get(f"{BASE_URL}/exercise", params={'language':2})
    data_exercises = resp.json()['results']
    return render_template('all_exercises.html', data_exercises=data_exercises)

@app.route('/exercise/<int:exercise_id>', methods=["GET"])
def show_exercise_info(exercise_id):
    resp = requests.get(f"{BASE_URL}/exercise", params={'language':2})
    data = resp.json()['results']
  
    res = None
    for exercise in data:
        if exercise['id'] == exercise_id:
            res = exercise
    return render_template('show_exercise.html', res=res)

# ________________________________________
# ----------------------------------------
# EXERCISE BY CATEGORY
# ----------------------------------------


resp = requests.get(f"{BASE_URL}/exercise", params={'language':2})
data_exercises = resp.json()['results']