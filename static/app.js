// _______________________________________________
// ===============================================
// in View Exercises
// Add Exercise to workout plan - *** WIP ***
// _______________________________________________
// on click 'Add to Workout'
$('.add-exercise-btn').click(addExercisetoPlan)

async function addExercisetoPlan() {
   const id = $(this).data('id')  // data-id="{{exercise['id']}}"
   await axios.get(`/exercise/${id}`)
}
// _______________________________________________
// ===============================================
// View Exercises by CATEGORY
// _______________________________________________
$('.dropdown-item').click(viewExerciseCategory)

function viewExerciseCategory() {
   alert("clicked!")
   const categoryId = $(this).data('category')
   alert(categoryId)
   return axios.get(`/exerciseby/category/${categoryId}`)
}