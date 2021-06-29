// Invite Patient Form
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
        $patient_id = $(this).attr('data-value')
        $('#btn_save_info').attr('data-value', $patient_id)
        console.log($patient_id)
        $is_editing = false

        var url = "/patients/info_upload"
        var formData = new FormData()
        var form = this
        formData.append('patient_id', $patient_id)

        $.ajax({
                type: 'POST',
                url: url,
                data: formData,
                processData: false,
                contentType: false,
                success: function(response){
                        if(response.message == 'ok'){
                            console.log('got ok')
                            $('#pi_first_name').val(response.first_name)
                            $('#pi_last_name').val(response.last_name)
                            $('#pi_email').val(response.email)
                            $('#pi_phone').val(response.phone_num)
                            $('#pi_sex').val(response.sex)
                            $('#pi_birth_date').val(new Date(response.birth_date).toString('yyyy-MM-dd'))
                            $('#pi_affected_side').val(response.affected_side[0].toUpperCase() + response.affected_side.slice(1))
                            $('#pi_angle_from').val(response.angle_limit_from)
                            $('#pi_angle_to').val(response.angle_limit_to)
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
        $('#invalid_affected_side_info').hide()
        $('#div_edit_info').attr("style", "display: block !important");
        $('#pi_affected_side').show();
        $('#pi_angle_from').show();
        $('#pi_angle_to').show();
        $('#angle_from_info')[0].setCustomValidity("");
        $('#angle_to_info')[0].setCustomValidity("");
    });


    $('#btn_edit_info').on("click", function(event) {
        $is_editing = true

        $('#select_affected_side_info').val($('#pi_affected_side').val()[0].toLowerCase() + $('#pi_affected_side').val().slice(1))
        $('#angle_from_info').val($('#pi_angle_from').val());
        $('#angle_to_info').val($('#pi_angle_to').val());

        $('#div_edit_info').attr("style", "display: none !important");
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


    $('#patient_info_form').on("submit", function(event) {
        event.preventDefault();
        if(!$('#select_affected_side_info').val())
        {
            $('#invalid_affected_side_info').show()
        }

        if(this.checkValidity())
        {
            var url = "/patients/info_save"
            var formData = new FormData()
            var form = this
            formData.append('patient_id', $('#btn_save_info').attr('data-value'))
            formData.append('affected_side', $('#select_affected_side_info').val())
            formData.append('angle_limit_from', $('#angle_from_info').val())
            formData.append('angle_limit_to', $('#angle_to_info').val())

            $.ajax({
                    type: 'POST',
                    url: url,
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function(response){
                            if(response.message == 'ok'){
                                console.log('got ok')
                                $('#pi_affected_side').val(response.affected_side[0].toUpperCase() + response.affected_side.slice(1))
                                $('#pi_angle_from').val(response.angle_limit_from)
                                $('#pi_angle_to').val(response.angle_limit_to)

                                $('#change_info_bar').hide()
                                $('#select_affected_side_info').hide()
                                $('#angle_from_info').hide()
                                $('#angle_to_info').hide()
                                $('#invalid_affected_side_info').hide()
                                $('#div_edit_info').attr("style", "display: block !important");
                                $('#pi_affected_side').show();
                                $('#pi_angle_from').show();
                                $('#pi_angle_to').show();
                                $('#angle_from_info')[0].setCustomValidity("");
                                $('#angle_to_info')[0].setCustomValidity("");

                                if($('#pi_angle_from').val() != 'Not Stated' && $('#pi_angle_to').val() != 'Not Stated')
                                {
                                    console.log('change')
                                    $('#angle_' + $('#btn_save_info').attr('data-value'))[0].innerHTML = 'Mobility Angle: ' + $('#pi_angle_from').val() + ' - ' + $('#pi_angle_to').val()
                                    $('#side_' + $('#btn_save_info').attr('data-value'))[0].innerHTML = 'Affected Side: ' + $('#pi_affected_side').val()
                                }
                            }
                            if(response.message == 'error'){

                                console.log('Can\'t upload Patient\'s info')
                            }},
                    error: function(response){
                            console.log('Can\'t send upload info request')
                           }
            });
        }
    });


    $('#btn_cancel_info').on('click', function(){
        $('#change_info_bar').hide()
        $('#select_affected_side_info').hide()
        $('#angle_from_info').hide()
        $('#angle_to_info').hide()
        $('#invalid_affected_side_info').hide()
        $('#div_edit_info').attr("style", "display: block !important");
        $('#pi_affected_side').show();
        $('#pi_angle_from').show();
        $('#pi_angle_to').show();
        $('#angle_from_info')[0].setCustomValidity("");
        $('#angle_to_info')[0].setCustomValidity("");
    })
});