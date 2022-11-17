from app import db
from models import User, Workouts, Exercise, ExerciseTracker

db.drop_all()
db.create_all()

