// Disabling form submissions if there are invalid fields
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


// All modal windows Validation func
$(document).ready(function () {
    $('.edit-modal-opener').click(function () {
        var url = $(this).data('whatever');
        $.get(url, function (data) {
            $('#Modal .modal-content').html(data);
            $('#Modal').modal();
            $('#submit').click(function (event) {
                event.preventDefault();
                $.post(url, data = $('#ModalForm').serialize(), function (
                    data) {
                    if (data.status == 'ok') {
                        $('#Modal').modal('hide');
                        location.reload();
                    } else {
                        var obj = JSON.parse(data);
                        for (var key in obj) {
                            if (obj.hasOwnProperty(key)) {
                                var value = obj[key];
                            }
                        }
                        $('.help-block').remove()
                        $('<p class="help-block">' + value + '</p>')
                            .insertAfter('#' + key);
                        $('.form-group').addClass('has-error')
                    }
                })
            });
        })
    });
});