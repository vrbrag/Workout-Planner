// =====================================================
// _________________/ *Exercise* Tab /__________________
// =====================================================
// _____________________________________________________
// Search Exercises by NAME
// _____________________________________________________
function myFunction() {
   // Declare variables
   let input, filter, table, tr, td, i, txtValue;
   input = document.getElementById("myInput");
   filter = input.value.toUpperCase();
   table = document.getElementById("exercisesTable");
   tr = table.getElementsByTagName("tr");

   // EXERCISE QUERY
   // Loop through all table rows, and hide those who don't match the search query
   for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
         txtValue = td.textContent || td.innerText;
         if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
         } else {
            tr[i].style.display = "none";
         }
      }
   }
}
// _____________________________________________________
// Add Exercise to workout plan - *** WIP ***
// _____________________________________________________
// on click 'Add to Workout'
$('.add-exercise-btn').click(addExercisetoPlan)

async function addExercisetoPlan() {
   const id = $(this).data('id')  // data-id="{{exercise['id']}}"
   await axios.get(`/exercise/${id}`)
}
// _____________________________________________________
// Search Exercises by CATEGORY - *** WIP ***
// _____________________________________________________
// $('.dropdown-item').click(viewExerciseCategory)

// function viewExerciseCategory() {
//    // alert("clicked!")
//    // const categoryId = $(this).data('value')
//    alert(categoryId)
//    return axios.get(`/exerciseby/category/${categoryId}`)
// }
