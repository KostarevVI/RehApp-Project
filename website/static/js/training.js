// Training form
$(document).ready(function () {
    var $exercise_type
    var $patient_selected = $('#select_patient').val()
    var $duration_value
    var $exercises_array = []

    $('#btn_Passive').on('click', function(e){
        $('#involvement_block').fadeOut(200)
        $('#timeout_block').fadeOut(200)
        $('#btn_add_exercise').addClass('btn-passive')
        $('#btn_add_exercise').removeClass('btn-active')
    });


    $('#btn_Active').on('click', function(e){
        $('#involvement_block').fadeIn(200);
        $('#timeout_block').fadeIn(200);
        $('#btn_add_exercise').addClass('btn-active')
        $('#btn_add_exercise').removeClass('btn-passive')
    });


    $('#select_patient').on('change', function (e) {
        $patient_selected = this.value;

        var url = "/training/change_patient"
        var formData = new FormData()

        formData.append('patient_id', $patient_selected)

        $.ajax({
                type: 'POST',
                url: url,
                data: formData,
                processData: false,
                contentType: false,
                success: function(response){
                        if(response.message == 'ok'){
                            console.log('got ok')
                            $('#angle_from').val(response.angle_limit_from)
                            $('#angle_to').val(response.angle_limit_to)
                        }
                        if(response.message == 'error'){
                            console.log('Can\'t upload Patient\'s info')
                        }},
                error: function(response){
                        console.log('Can\'t send upload info request')
                       }
        });
    });


    var angle_and_rep_validation_func = function(){

        if(($('#angle_from').val().length == 0) || ($('#angle_from').val() == ''))
        {
            $('#angle_from')[0].setCustomValidity("error");
            $('#invalid_angle_from').text('Angle must be from 0 to 135.');
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
            else if((/^[0-9]+$/.test($('#angle_to').val())) && (parseInt($('#angle_from').val()) >= parseInt($('#angle_to').val())))
            {
                $('#angle_from')[0].setCustomValidity("error");
                $('#invalid_angle_from').text('From angle <= To angle.');
            }
            else
            {
                $('#angle_from')[0].setCustomValidity("");
            }
        }


        if(($('#angle_to').val().length == 0) || ($('#angle_to').val() == ''))
        {
            $('#angle_to')[0].setCustomValidity("error");
            $('#invalid_angle_to').text('Angle must be from 0 to 135.');
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


        if(($('#repetitions').val().length == 0) || ($('#repetitions').val() == ''))
        {
            $('#repetitions')[0].setCustomValidity("error");
            $('#invalid_repetitions').text('Reps must be from 1 to 50.');
        }
        else if(!/^[0-9]+$/.test($('#repetitions').val()))
        {
            $('#repetitions')[0].setCustomValidity("error");
            $('#invalid_repetitions').text('Don\'t use symbols.');
        }
        else
        {
            if($('#repetitions').val().length > 1 && $('#repetitions').val()[0] == '0')
            {
                $('#repetitions')[0].setCustomValidity("error");
                $('#invalid_repetitions').text('\'0\' at the beginning.');
            }
            else if(parseInt($('#repetitions').val()) > 50)
            {
                $('#repetitions')[0].setCustomValidity("error");
                $('#invalid_repetitions').text('Max reps is 50.');
            }
            else if(parseInt($('#repetitions').val()) < 1)
            {
                $('#repetitions')[0].setCustomValidity("error");
                $('#invalid_repetitions').text('Min reps is 1.');
            }
            else
            {
                $('#repetitions')[0].setCustomValidity("");
            }
        }


        if($('#exercise_form')[0].checkValidity())
        {

            var raw_time = ((0.11852 - (parseInt($('#select_speed').val()) - 1) * 0.00741) *
                (parseInt($('#angle_to').val()) - parseInt($('#angle_from').val())) * parseInt($('#repetitions').val()) +
                parseInt($('#repetitions').val()) * 0.5) * 2 // Расчёт примерного времени на основе замеров с тренажёра
            var minutes = Math.floor(raw_time / 60);
            var seconds = (raw_time - minutes * 60).toFixed();
            $duration_value = (minutes < 10 ? "0" : "") + minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
            console.log(parseInt($('#angle_to').val()) + ' ' + raw_time + ' ' + minutes + ' ' + seconds + ' ' + $duration_value)
            $('#duration').val($duration_value);
        }
        else
        {
            console.log('invalid')
            $('#duration').val('00:00')
        }
    };


    $('#exercise_form').on("keyup change", angle_and_rep_validation_func)


    $('#exercise_form').on('submit', function(event){
        event.preventDefault()
        if(this.checkValidity())
        {
            $exercises_array.push({
                order_in_training: $exercises_array.length + 1,
                type: $('input[name="exercise_form-type"]:checked').val(),
                speed: $('#select_speed').val(),
                angle_limit_from: $('#angle_from').val(),
                angle_limit_to: $('#angle_to').val(),
                repetitions: $('#repetitions').val(),
                spasms_stop_value: $('#spasms_stop_value').val(),
                involvement: $('#select_involvement').val(),
                repetition_timeout: $('#select_timeout').val(),
                duration: $('#duration').val()
            })
            console.log($exercises_array)


            $('#total_pass_exercises')
            $('#total_pass_reps')
            $('#total_pass_duration')
            $('#total_act_exercises')
            $('#total_act_reps')
            $('#total_act_duration')
            $('#total_exercises')
            $('#total_reps')
            $('#total_duration')
        }
    });


    $('#training_form').on('submit', function(event){
        event.preventDefault()
        if(this.checkValidity())
        {
            var url = "/training/send_training"

            var unindexed_array = $('#training_form').serializeArray();
            var indexed_array = {};

            $.map(unindexed_array, function(n, i){
                indexed_array[n['name']] = n['value'];
            });

            var json_data = {
                                'training_info':indexed_array,
                                'exercises_array':$exercises_array
                            }

            console.log(JSON.stringify(json_data))

            $.ajax({
                    type: 'POST',
                    url: url,
                    data: JSON.stringify(json_data),
                    processData: false,
                    contentType: "application/json",
                    success: function(response){
                            if(response.message == 'ok'){
                                console.log('got ok')
                                console.log(response.data)
                                //$(location).attr('href', response.url);
                            }
                            if(response.message == 'error'){
                                console.log('Can\'t send training to Patient')
                                console.log(response.data)
                            }},
                    error: function(response){
                            console.log('Bad Request')
                           }
            });
        }
    });
});