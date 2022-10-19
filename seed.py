from app import db
from models import User, Workouts, Exercise, ExerciseTracker

db.drop_all()
db.create_all()

# User.query.delete()
# user_1 = User(
#    username = 'mickeyMouse',
#    email = 'mickeymouse@yahoo.com',
#    password = 123456
# )

# Workouts.query.delete()
# workout_1 = Workouts(
#    # id = 1
#    name = 'Glutes/Quads',
#    # day = 'Monday',
#    exercise_id = 1, 
#    # tracker_id = 1,
#    user_id = 1
# )
# workout_2 = Workouts(
#    # id = 2
#    name = 'Shoulders/Chest/Tris',
#    # day = 'Tuesday',
#    exercise_id = 2, 
#    # tracker_id = 2,
#    user_id = 1
# )
# workout_3 = Workouts(
#    # id = 3
#    name = 'Glutes/Hamstrings',
#    # day = 'Thursday',
#    exercise_id = 3, 
#    # tracker_id = 3,
#    user_id = 1
# )
# workout_4 = Workouts(
#    # id = 4
#    name = 'Back/Bis',
#    # day = 'Friday',
#    exercise_id = 4, 
#    # tracker_id = 4,
#    user_id = 1
# )
# workout_5 = Workouts(
#    # id = 5
#    name = 'Back/Bis',
#    # day = 'Friday',
#    exercise_id = 5, 
#    # tracker_id = 5,
#    user_id = 1
# )

Exercise.query.delete()
exercise_1 = Exercise(
   # id = 1
   name = 'Sumo Squat',
   description = 'Wide stance, hold dumbbell between legs and squat',
   category = 9,
   equipment = 1,
   variations = 111
)
exercise_2 = Exercise(
   # id = 2
   name = 'Shoulder Shrug',
   description = 'The shoulder shrug (usually called simply the shrug) is an exercise in weight training used to develop the upper trapezius muscle. The lifter stands erect, hands about shoulder width apart, and raises the shoulders as high as possible, and then lowers them, while not bending the elbows, or moving the body at all.',
   category = 13,
   equipment = 2,
   variations = 222
)
exercise_3 = Exercise(
   # id = 3
   name = 'Leg Curl',
   description = 'The leg curl, also known as the hamstring curl, is an isolation exercise that targets the hamstring muscles. The exercise involves flexing the lower leg against resistance towards the buttocks.',
   category = 9,
   equipment = 3,
   variations = 333
)
exercise_4 = Exercise(
   # id = 4
   name = 'Bicep Curls With Barbell',
   description = 'Hold the Barbell shoulder-wide, the back is straight, the shoulders slightly back, the arms are streched. Bend the arms, bringing the weight up, with a fast movement. Without pausing, let down the bar with a slow and controlled movement.',
   category = 8,
   equipment = 4,
   variations = 444
)
exercise_5 = Exercise(
   # id = 5
   name = 'Lat Pull Down',
   description = 'Lean Back, Pull into chest',
   category = 12,
   equipment = 5,
   variations = 555
)

# ExerciseTracker.query.delete()
# tracker_1 = ExerciseTracker(
#    # id = 1
#    workout_id = 1,
#    sets = 4,
#    reps = 10,
#    weight = 25,
# )
# tracker_2 = ExerciseTracker(
#    # id = 2
#    workout_id = 2,
#    sets = 4,
#    reps = 10,
#    weight = 25,
# )
# tracker_3 = ExerciseTracker(
#    # id = 3
#    workout_id = 3,
#    sets = 4,
#    reps = 10,
#    weight = 25,
# )
# tracker_4 = ExerciseTracker(
#    # id = 4
#    workout_id = 4,
#    sets = 4,
#    reps = 10,
#    weight = 25,
# )
# tracker_5 = ExerciseTracker(
#    # id = 5
#    workout_id = 5,
#    sets = 4,
#    reps = 10,
#    weight = 25,
# )


db.session.add_all([exercise_1, exercise_2, exercise_3,exercise_4, exercise_5])
db.session.commit()