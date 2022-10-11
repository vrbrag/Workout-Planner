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

# @app.route("/exerciseby")
# def get_exercises():
#     category = request.args["category"]
#     resp = requests.get(f"{BASE_URL}/exercise", params={'language':2, 'category': category})
#     data = resp.json()['results']
#     return render_template('exerciseby.html', data=data)

def exerciseBy(cat):
    resp = requests.get(f"{BASE_URL}/exercise", params={'language':2, 'category': cat})
    data = resp.json()['results']
    return data

@app.route("/")
def homepage():

    return render_template('base.html')

## by ABS
@app.route("/exercisebyabs")
def get_abs_exercises():
    """Category ABS == 10 """
    data = exerciseBy(10)

    return render_template('category.html', data=data, name="Abs")

## by ARMS
@app.route("/exercisebyarms")
def get_arms_exercises():
    """Category ARMS == 8 """
    data = exerciseBy(8)
    
    return render_template('category.html', data=data, name="Arms")

## by BACK
@app.route("/exercisebyback")
def get_back_exercises():
    """Category BACK == 12 """
    data = exerciseBy(12)
    
    return render_template('category.html', data=data, name="Back")

## by CALVES
@app.route("/exercisebycalves")
def get_calves_exercises():
    """Category CALVES == 14 """
    data = exerciseBy(14)
    
    return render_template('category.html', data=data, name="Calves")

## by CHEST
@app.route("/exercisebychest")
def get_chest_exercises():
    """Category CHEST == 11 """
    data = exerciseBy(11)
    
    return render_template('category.html', data=data, name="Chest")

## by LEGS
@app.route("/exercisebylegs")
def get_legs_exercises():
    """Category LEGS == 9 """
    data = exerciseBy(9)

    return render_template('category.html', data=data, name="Legs")

## by SHOULDERS
@app.route("/exercisebyshoulders")
def get_shoulders_exercises():
    """Category SHOULDERS == 13 """
    data = exerciseBy(13)
    
    return render_template('category.html', data=data, name="Shoulders")