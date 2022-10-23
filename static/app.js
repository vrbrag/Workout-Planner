// =====================================================
// _________________/ *Exercise* Tab /__________________
// =====================================================
// _____________________________________________________
// Search Exercises by NAME
// _____________________________________________________
function searchExercises() {
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

// =====================================================
// _________________/ *Workout* Tab /__________________
// =====================================================
// _____________________________________________________
// Save Exercise to exercise table 
// _____________________________________________________
// on click 'Add to my Exercises table'
$('.save-exercise-btn').click(saveExercise)

async function saveExercise() {
   const id = $(this).data('id')  // data-id="{{exercise['id']}}"
   // alert(`id: ${id}`)
   await axios.get(`/exercise/${id}`)
   $(this).remove()
}
// _____________________________________________________
// Add Exercise to Workout
// _____________________________________________________
// on click 'Add exercise to workout list'
$('.add-exercise-btn').click(addToWorkout)

async function addToWorkout() {
   let name = $('#add-exercise').find('option:selected').text()
   let newOption = $('<option></option>').attr("selected", "selected");
   newOption.val(name);
   newOption.html(name);
   // $("#add-exercise option:selected").remove();
   $('.selected-workout-list').append('<li>' + name + '<button type="button" class="delete btn btn-danger btn-sm pull-right">Remove</button></li>')
}

$("body").on("click", ".delete", function () {
   $(this).parent().remove();
})
