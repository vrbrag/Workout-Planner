from app import db
from models import WorkoutSession, Exercise

db.drop_all()
db.create_all()

Workout.query.delete()
workout_1 = WorkoutSession(
   # id = 1
   name = 'Glutes/Quads'
)
workout_2 = WorkoutSession(
   # id = 2
   name = 'Shoulders/Chest/Tris'
)
workout_3 = WorkoutSession(
   # id = 3
   name = 'Glutes/Hamstrings'
)
workout_4 = WorkoutSession(
   # id = 4
   name = 'Back/Bis',
)



db.session.add_all([workout_1, workout_2, workout_3,workout_4])
db.session.commit()