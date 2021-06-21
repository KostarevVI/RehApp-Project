function deletePerson(personId) {
  fetch("/delete-person", {
    method: "POST",
    body: JSON.stringify({ personId: personId }),
  }).then((_res) => {
    window.location.href = "/";
  });
};


function playPerson(playPersonId) {
  fetch("/play-person", {
    method: "POST",
    body: JSON.stringify({ playPersonId: playPersonId }),
  }).then((_res) => {
    window.location.href = "/play";
  });
};


function inventorySelect() {
  var perInv1 = $("#inventoriesSelect1 option:selected").val();
  var perInv2 = $("#inventoriesSelect2 option:selected").val();
  fetch("/inventory-select", {
    method: "POST",
    body: JSON.stringify({ perInv1: perInv1,
                           perInv2: perInv2 }),
  }).then((_res) => {
    window.location.href = "/inventory";
  });
};


// Example starter JavaScript for disabling form submissions if there are invalid fields
(function() {
  'use strict';

    window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();

//function createPerson() {
//
//  fetch("/create-person", {
//    method: "POST",
//    body: JSON.stringify({ selectedClass: selectedClass }),
//  }).then((_res) => {
//    window.location.href = "/";
//  });
//  alert(selectedClass);
//}