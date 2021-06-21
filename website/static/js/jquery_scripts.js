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


// Reset Password Change From
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


// Invite Patient From
$(document).ready(function () {
    $('#angle_bar').hide()

    $('#add_angle_info').on("click", function(event) {
        if($('#add_angle_info').is(':checked'))
        {
            $('#angle_bar').slideDown();
            $('#angle_from').prop('disabled', false);
            $('#angle_to').prop('disabled', false);
            $('#select_affected_side').prop('disabled', false);
        }
        else
        {
            $('#angle_bar').slideUp();
            $('#angle_from').prop('disabled', true);
            $('#angle_to').prop('disabled', true);
            $('#select_affected_side').prop('disabled', true);
        }
    });

    $('#invite_patient_form').on("keyup", function(event) {
        if($('#add_angle_info').is(':checked')){
            if(($('#angle_from').val().length == 0) || ($('#angle_from').val() == ''))
            {
                $('#angle_from')[0].setCustomValidity("error");
                $('#invalid_angle_from').text('Enter Value.');
            }
            else if(!/^[0-9]+$/.test($('#angle_from').val()))
            {
                $('#angle_from')[0].setCustomValidity("error");
                $('#invalid_angle_from').text('Don\'t use symbols.');
            }
            else
            {
                if($('#angle_from').val().length > 1 && $('#angle_from').val()[0] == '0')
                {
                    $('#angle_from')[0].setCustomValidity("error");
                    $('#invalid_angle_from').text('\'0\' at the beginning.');
                }
                else if(parseInt($('#angle_from').val()) > 135)
                {
                    $('#angle_from')[0].setCustomValidity("error");
                    $('#invalid_angle_from').text('Max angle is 135.');
                }
                else if((/^[0-9]+$/.test($('#angle_to').val())) && (parseInt($('#angle_from').val()) > parseInt($('#angle_to').val())))
                {
                    $('#angle_from')[0].setCustomValidity("error");
                    $('#invalid_angle_from').text('From angle < To angle.');
                }
                else
                {
                    $('#angle_from')[0].setCustomValidity("");
                }
            }


            if(($('#angle_to').val().length == 0) || ($('#angle_to').val() == ''))
            {
                $('#angle_to')[0].setCustomValidity("error");
                $('#invalid_angle_to').text('Enter Value.');
            }
            else if(!/^[0-9]+$/.test($('#angle_to').val()))
            {
                $('#angle_to')[0].setCustomValidity("error");
                $('#invalid_angle_to').text('Don\'t use symbols.');
            }
            else
            {
                if($('#angle_to').val().length > 1 && $('#angle_to').val()[0] == '0')
                {
                    $('#angle_to')[0].setCustomValidity("error");
                    $('#invalid_angle_to').text('\'0\' at the beginning.');
                }
                else if(parseInt($('#angle_to').val()) > 135)
                {
                    $('#angle_to')[0].setCustomValidity("error");
                    $('#invalid_angle_to').text('Max angle is 135.');
                }
                else if((/^[0-9]+$/.test($('#angle_from').val())) && (parseInt($('#angle_from').val()) > parseInt($('#angle_to').val())))
                {
                    $('#angle_to')[0].setCustomValidity("error");
                    $('#invalid_angle_to').text('');
                }
                else
                {
                    $('#angle_to')[0].setCustomValidity("");
                }
            }
        }
        else
        {
            $('#angle_from')[0].setCustomValidity("");
            $('#angle_to')[0].setCustomValidity("");
        }
    });


    $('#invite_patient_form').on("submit", function(event) {
        event.preventDefault();
        if(this.checkValidity())
        {
          $('#loading').fadeIn(400);
          $('#spinner').fadeIn(400);
          this.submit()
        }
    });
});


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


// Patient Info Upload
$(document).ready(function () {
    var $patient_id
    var $is_editing = false


    var angle_validation_func = function(){
        if($is_editing)
        {
            console.log('Start validation angle')
            if(($('#angle_from_info').val().length == 0) || ($('#angle_from_info').val() == ''))
            {
                $('#angle_from_info')[0].setCustomValidity("error");
                $('#invalid_angle_from_info').text('Enter Value.');
            }
            else if(!/^[0-9]+$/.test($('#angle_from_info').val()))
            {
                $('#angle_from_info')[0].setCustomValidity("error");
                $('#invalid_angle_from_info').text('Don\'t use symbols.');
            }
            else
            {
                if($('#angle_from_info').val().length > 1 && $('#angle_from_info').val()[0] == '0')
                {
                    $('#angle_from_info')[0].setCustomValidity("error");
                    $('#invalid_angle_from_info').text('\'0\' at the beginning.');
                }
                else if(parseInt($('#angle_from_info').val()) > 135)
                {
                    $('#angle_from_info')[0].setCustomValidity("error");
                    $('#invalid_angle_from_info').text('Max angle is 135.');
                }
                else if((/^[0-9]+$/.test($('#angle_to_info').val())) && (parseInt($('#angle_from_info').val()) > parseInt($('#angle_to_info').val())))
                {
                    $('#angle_from_info')[0].setCustomValidity("error");
                    $('#invalid_angle_from_info').text('From angle < To angle.');
                }
                else
                {
                    $('#angle_from_info')[0].setCustomValidity("");
                }
            }

            if(($('#angle_to_info').val().length == 0) || ($('#angle_to_info').val() == ''))
            {
                $('#angle_to_info')[0].setCustomValidity("error");
                $('#invalid_angle_to_info').text('Enter Value.');
            }
            else if(!/^[0-9]+$/.test($('#angle_to_info').val()))
            {
                $('#angle_to_info')[0].setCustomValidity("error");
                $('#invalid_angle_to_info').text('Don\'t use symbols.');
            }
            else
            {
                if($('#angle_to_info').val().length > 1 && $('#angle_to_info').val()[0] == '0')
                {
                    $('#angle_to_info')[0].setCustomValidity("error");
                    $('#invalid_angle_to_info').text('\'0\' at the beginning.');
                }
                else if(parseInt($('#angle_to_info').val()) > 135)
                {
                    $('#angle_to_info')[0].setCustomValidity("error");
                    $('#invalid_angle_to_info').text('Max angle is 135.');
                }
                else if((/^[0-9]+$/.test($('#angle_from_info').val())) && (parseInt($('#angle_from_info').val()) > parseInt($('#angle_to_info').val())))
                {
                    $('#angle_to_info')[0].setCustomValidity("error");
                    $('#invalid_angle_to_info').text('');
                }
                else
                {
                    $('#angle_to_info')[0].setCustomValidity("");
                }
            }
        }
    }


    $('.btn-more-info').on("click", function(event) {
        $patient_id = this.value
        console.log($patient_id)
        $is_editing = false

        var url = "/patients/info_upload"
        var formData = new FormData()
        var form = this
        formData.append('patient_id', $patient_id)

//        console.log(grecaptcha.getResponse())

        $.ajax({
                type: 'POST',
                url: url,
                data: formData,
                processData: false,
                contentType: false,
                success: function(response){
                        if(response.message == 'ok'){

                            console.log('got ok' + response.data)

                        }
                        if(response.message == 'error'){
                            //handle flask-wtf errors here

                            console.log('Can\'t upload Patient\'s info')
                        }},
                error: function(response){
                        console.log('Can\'t send upload info request')
                       }
        })

        $('#change_info_bar').hide()
        $('#select_affected_side_info').hide()
        $('#angle_from_info').hide()
        $('#angle_to_info').hide()
        $('#btn_edit_info').attr("style", "display: block !important");
        $('#pi_affected_side').show();
        $('#pi_angle_from').show();
        $('#pi_angle_to').show();
        $('#angle_from_info').val("");
        $('#angle_to_info').val("");
        $('#angle_from_info')[0].setCustomValidity("");
        $('#angle_to_info')[0].setCustomValidity("");
    });


    $('#btn_edit_info').on("click", function(event) {
        $is_editing = true
        $('#btn_edit_info').attr("style", "display: none !important");
        $('#pi_affected_side').hide();
        $('#pi_angle_from').hide();
        $('#pi_angle_to').hide();

        $('#change_info_bar').show()
        $('#select_affected_side_info').show()
        $('#angle_from_info').show()
        $('#angle_to_info').show()
        angle_validation_func()
    });


    $('#patient_info_form').on("keyup", angle_validation_func)
});


//$(document).ready(function() {
//        $('#myTable').DataTable();
//
//});
//$(document).ready(function() {
//    $('#myTable').dataTable( {
//      "scrollY": "200px",
//      "scrollCollapse": true,
//      "paging": false
//      "searching": false
//      "ordering": false
//    } );
//});