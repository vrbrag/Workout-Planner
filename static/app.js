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

