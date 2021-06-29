// Therapist Sign Up Form
$(document).ready(function () {
   $('#req_form').on("keyup", function(event) {
      if(!$('#req_first_name').val())
      {
        $('#req_first_name')[0].setCustomValidity("error");
        $('#invalid_first_name').text('Please enter First Name.');
      }
      else if (($('#req_first_name').val().length > 30) && ($('#req_first_name').val() != ''))
      {
        $('#req_first_name')[0].setCustomValidity("error");
        $('#invalid_first_name').text('First Name is too long.');
      }
      else if (!/^[а-яА-Яa-zA-Z]+$/.test($('#req_first_name').val()))
      {
        $('#req_first_name')[0].setCustomValidity("error");
        $('#invalid_first_name').text('Please don\'t use symbols or numbers.');
      }
      else
      {
        $('#req_first_name')[0].setCustomValidity("");
      }


      if(!$('#req_last_name').val())
      {
        $('#req_last_name')[0].setCustomValidity("error");
        $('#invalid_last_name').text('Please enter Last Name..');
      }
      else if (($('#req_last_name').val().length > 30) && ($('#req_last_name').val() != ''))
      {
        $('#req_last_name')[0].setCustomValidity("error");
        $('#invalid_last_name').text('Last Name is too long.');
      }
      else if (!/^[а-яА-Яa-zA-Z]+$/.test($('#req_last_name').val()))
      {
        $('#req_last_name')[0].setCustomValidity("error");
        $('#invalid_last_name').text('Please don\'t use symbols or numbers.');
      }
      else
      {
        $('#req_last_name')[0].setCustomValidity("");
      }


      if(($('#req_phone').val() == '') && ($('#req_phone').val().length == 0))
      {
        $('#req_phone')[0].setCustomValidity("error");
        $('#invalid_phone_num').text('Please enter Phone Number without symbols.');
      }
      else if (($('#req_phone').val().length > 20) && ($('#req_phone').val() != ''))
      {
        $('#req_phone')[0].setCustomValidity("error");
        $('#invalid_phone_num').text('Phone Number is too long.');
      }
      else if (!/^[0-9]+$/.test(String($('#req_phone').val())))
      {
        $('#req_phone')[0].setCustomValidity("error");
        $('#invalid_phone_num').text('Please enter Phone Number without symbols.');
      }
      else
      {
        $('#req_phone')[0].setCustomValidity("");
      }


      if(!$('#req_pass').val())
      {
        $('#req_pass')[0].setCustomValidity("error");
        $('#invalid_req_pass').text('Please enter Password.');
      }
      else if(($('#req_pass').val().length < 8) && ($('#req_pass').val() != ''))
      {
        $('#req_pass')[0].setCustomValidity("error");
        $('#invalid_req_pass').text('Password must be greater than 8 characters.');
      }
      else if (($('#req_pass').val().length > 80) && ($('#req_pass').val() != ''))
      {
        $('#req_pass')[0].setCustomValidity("error");
        $('#invalid_req_pass').text('Password must be less than 80 characters.');
      }
      else {
        $('#req_pass')[0].setCustomValidity("");
      }

      if(($('#req_conf_pass').val() != $('#req_pass').val()) && ($('#req_conf_pass').val() != ''))
      {
        $('#req_conf_pass')[0].setCustomValidity("error");
        $('#invalid_conf').text('Passwords must match.');
      }
      else if(($('#req_conf_pass').val() == $('#req_pass').val()))
      {
        $('#req_conf_pass')[0].setCustomValidity("");
      }
    });


    $('#req_form').on("submit", function(event) {
        event.preventDefault();

        var url = "/recaptcha_verify"
        var formData = new FormData()
        var form = this
        formData.append('g-recaptcha-response', grecaptcha.getResponse())

//        console.log(grecaptcha.getResponse())

        $.ajax({
                type: 'POST',
                url: url,
                data: formData,
                processData: false,
                contentType: false,
                success: function(response){
                        grecaptcha.reset() //recaptcha reset
                        if(response.message == 'ok'){
                            $('#req_recaptcha_error')[0].setCustomValidity("");
                            console.log('got ok')
                            if(form.checkValidity())
                            {
                              $('#loading').fadeIn(400);
                              $('#spinner').fadeIn(400);
                              form.submit()
                            }
                        }
                        if(response.message == 'error'){
                            //handle flask-wtf errors here
                            $('#req_recaptcha_error')[0].setCustomValidity("error");
                            console.log('Captcha isn\'t complete error')
                        }},
                error: function(response){
                        grecaptcha.reset()
                        console.log('Can\'t validate recaptcha error')
                       }
        })
    });
});


// Reset Password Request Form
$(document).ready(function () {
    $('#pass_res_form').on("submit", function(event) {
        event.preventDefault();
        if(this.checkValidity())
        {
            $('#loading').fadeIn(400);
            $('#spinner').fadeIn(400);
            this.submit()
        }
    });
});


// Reset Password Change Form
$(document).ready(function () {
   $('#pass_res_form_form').on("keyup", function(event) {
      if(($('#pass_res_form_pass').val().length == 0) && ($('#pass_res_form_pass').val() == ''))
      {
        $('#pass_res_form_pass')[0].setCustomValidity("error");
        $('#invalid_pass_res_pass').text('Please enter Password.');
      }
      else if(($('#pass_res_form_pass').val().length < 8) && ($('#pass_res_form_pass').val() != ''))
      {
        $('#pass_res_form_pass')[0].setCustomValidity("error");
        $('#invalid_pass_res_pass').text('Password must be greater than 8 characters.');
      }
      else if (($('#pass_res_form_pass').val().length > 80) && ($('#pass_res_form_pass').val() != ''))
      {
        $('#pass_res_form_pass')[0].setCustomValidity("error");
        $('#invalid_pass_res_pass').text('Password must be less than 80 characters.');
      }
      else {
        $('#pass_res_form_pass')[0].setCustomValidity("");
      }

      if(($('#pass_res_form_conf').val() != $('#pass_res_form_pass').val()) && ($('#pass_res_form_conf').val() != ''))
      {
        $('#pass_res_form_conf')[0].setCustomValidity("error1");
        $('#invalid_pass_res_conf').text('Passwords must match.');
      }
      else if(($('#pass_res_form_conf').val() == $('#pass_res_form_pass').val()))
      {
        $('#pass_res_form_conf')[0].setCustomValidity("");
      }
    });

    $('#pass_res_form_form').on("submit", function(event) {
        event.preventDefault();
        if(this.checkValidity())
        {
          $('#loading').fadeIn(400);
          $('#spinner').fadeIn(400);
          this.submit()
        }
    });
});