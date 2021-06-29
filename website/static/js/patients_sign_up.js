// Patient Sign Up
$(document).ready(function () {
   $('#pat_form').on("keyup", function(event) {
      if(!$('#pat_first_name').val())
      {
        $('#pat_first_name')[0].setCustomValidity("error");
        $('#invalid_pat_first_name').text('Please enter First Name.');
      }
      else if (($('#pat_first_name').val().length > 30) && ($('#pat_first_name').val() != ''))
      {
        $('#pat_first_name')[0].setCustomValidity("error");
        $('#invalid_pat_first_name').text('First Name is too long.');
      }
      else if (!/^[а-яА-Яa-zA-Z]+$/.test($('#pat_first_name').val()))
      {
        $('#pat_first_name')[0].setCustomValidity("error");
        $('#invalid_pat_first_name').text('Please don\'t use symbols or numbers.');
      }
      else
      {
        $('#pat_first_name')[0].setCustomValidity("");
      }


      if(!$('#pat_last_name').val())
      {
        $('#pat_last_name')[0].setCustomValidity("error");
        $('#invalid_pat_last_name').text('Please enter Last Name..');
      }
      else if (($('#pat_last_name').val().length > 30) && ($('#pat_last_name').val() != ''))
      {
        $('#pat_last_name')[0].setCustomValidity("error");
        $('#invalid_pat_last_name').text('Last Name is too long.');
      }
      else if (!/^[а-яА-Яa-zA-Z]+$/.test($('#pat_last_name').val()))
      {
        $('#pat_last_name')[0].setCustomValidity("error");
        $('#invalid_pat_last_name').text('Please don\'t use symbols or numbers.');
      }
      else
      {
        $('#pat_last_name')[0].setCustomValidity("");
      }


      if(($('#pat_phone').val() == '') && ($('#pat_phone').val().length == 0))
      {
        $('#pat_phone')[0].setCustomValidity("error");
        $('#invalid_pat_phone_num').text('Please enter Phone Number without symbols.');
      }
      else if (($('#pat_phone').val().length > 20) && ($('#pat_phone').val() != ''))
      {
        $('#pat_phone')[0].setCustomValidity("error");
        $('#invalid_pat_phone_num').text('Phone Number is too long.');
      }
      else if (!/^[0-9]+$/.test(String($('#pat_phone').val())))
      {
        $('#pat_phone')[0].setCustomValidity("error");
        $('#invalid_pat_phone_num').text('Please enter Phone Number without symbols.');
      }
      else
      {
        $('#pat_phone')[0].setCustomValidity("");
      }


      if(!$('#pat_pass').val())
      {
        $('#pat_pass')[0].setCustomValidity("error");
        $('#invalid_pat_pass').text('Please enter Password.');
      }
      else if(($('#pat_pass').val().length < 8) && ($('#pat_pass').val() != ''))
      {
        $('#pat_pass')[0].setCustomValidity("error");
        $('#invalid_pat_pass').text('Password must be greater than 8 characters.');
      }
      else if (($('#pat_pass').val().length > 80) && ($('#pat_pass').val() != ''))
      {
        $('#pat_pass')[0].setCustomValidity("error");
        $('#invalid_pat_pass').text('Password must be less than 80 characters.');
      }
      else {
        $('#pat_pass')[0].setCustomValidity("");
      }

      if(($('#pat_conf_pass').val() != $('#pat_pass').val()) && ($('#pat_conf_pass').val() != ''))
      {
        $('#pat_conf_pass')[0].setCustomValidity("error");
        $('#invalid_pat_conf').text('Passwords must match.');
      }
      else if(($('#pat_conf_pass').val() == $('#pat_pass').val()))
      {
        $('#pat_conf_pass')[0].setCustomValidity("");
      }
    });


    $('#pat_form').on("submit", function(event) {
        event.preventDefault();
        if(this.checkValidity())
        {
          $("#pat_email").prop('disabled', false);
          $("#pat_therapist_id").prop('disabled', false);
          $("#pat_angle_from").prop('disabled', false);
          $("#pat_angle_to").prop('disabled', false);
          $("#pat_affected_side").prop('disabled', false);
          $('#loading').fadeIn(400);
          $('#spinner').fadeIn(400);
          this.submit()
        }
    });
});