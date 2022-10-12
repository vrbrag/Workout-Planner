// _______________________________________________
// ===============================================
// Add Exercise to workout plan - *** WIP ***
// _______________________________________________
// on click 'Add to Workout'
$('.add-exercise-btn').click(addExercisetoPlan)

async function addExercisetoPlan() {
   const id = $(this).data('id')  // data-id="{{exercise['id']}}"
   await axios.get(`/exercise/${id}`)
}
// _______________________________________________