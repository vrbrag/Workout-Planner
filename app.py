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

    return render_template('base.html')

@app.route("/exerciseby")
def exercise_by():

    return render_template('testexercise.html')

@app.route("/exercisecategory")
def get_exercises():
    category = request.args["category"]
    resp = requests.get(f"{BASE_URL}/exercise", params={'language':2, 'category': category})

    data = resp.json()['results']
    for i in range(len(data)):
        name = data[i]['name']
        description = data[i]['description'] 
        equipment = data[i]['equipment'] 
        variations = data[i]['variations'] 
        
        
    # new_dict = {}
    # for dic in data:
    #     for key, val in dic.items():
    #         new_dict[key] = val
            # for i in keys:
            #     if i == key:
                    
            #         new_dict[key] = val
                    # new_list = list(new_dict)
                    # new_key = list(new_dict.keys())
                    # new_val = list(new_dict.values())
                    # exercises = {'key' : new_key, 'val' : new_val}
    

    return render_template('testexercise.html', name=name, description=description, equipment=equipment, variations=variations)



##### exercise by category : 10 == Abs
##### specifically want keys: 'name', 'description', 'equipment', 'variations'
resp = requests.get(f"{BASE_URL}/exercise", params={'language':2, 'category': 10})

data = resp.json()['results']
for i in range(len(data)):
    # print(i)
    name = data[i]['name']
    description = data[i]['description']
    equipment = data[i]['equipment']
    variations = data[i]['variations']


    print("------------------------")
    print(f"NAME: {name}")
    print(f"DESCRIPTION: {description}")
    print(f"EQUIPMENT: {equipment}")
    print(f"VARIATIONS: {variations}")
    print("------------------------")
    
    


    # keys = ['name', 'description']
    # new_dict = {}
    # for dic in data:
    #     for key, val in dic.items():
    #         new_dict[key] = val
    #         print(new_dict)