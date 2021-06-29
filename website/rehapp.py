from datetime import datetime, timedelta, date
import time
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from website.models import *
from .__name__ import db, mail
from flask_login import login_user, login_required, logout_user, current_user
from .forms import InvitePatient, PatientInfoChange, TrainingForm, ExerciseForm
from flask_mail import Message
from .async_email import send_email

from sqlalchemy import *

rehapp = Blueprint('rehapp', __name__)


@rehapp.route('/dash', methods=['GET', 'POST'])
@login_required
def dashboard():
    patients_with_trainings = \
        db.session.query(Training).join(Patient, Training.patient_id == Patient.id) \
            .join(PatientOfTherapist, PatientOfTherapist.patient_id == Patient.id) \
            .filter(PatientOfTherapist.therapist_id == current_user.id).filter(Training.execution_date < datetime.now()) \
            .filter(Training.execution_date > datetime.now() - timedelta(weeks=4)) \
            .order_by(Training.execution_date.desc()).all()

    print(patients_with_trainings if patients_with_trainings else False)

    return render_template('dashboard.html', title='Dashboard', current_user=current_user,
                           patients_with_trainings=patients_with_trainings)


@rehapp.route('/patients', methods=['GET', 'POST'])
@login_required
def patients():
    invite_patient = InvitePatient(prefix="invite_patient")
    patient_info_change = PatientInfoChange(prefix="patient_info_change")

    patients_of_therapist = \
        db.session.query(Patient).join(PatientOfTherapist, PatientOfTherapist.patient_id == Patient.id) \
            .filter(PatientOfTherapist.therapist_id == current_user.id) \
            .order_by(PatientOfTherapist.therapy_start_date.desc()).all()

    return render_template('patients.html', title='Patients', current_user=current_user,
                           patients_of_therapist=patients_of_therapist, invite_patient=invite_patient,
                           patient_info_change=patient_info_change)


@rehapp.route('/patients/invite', methods=['GET', 'POST'])
@login_required
def invite_patient_handler():
    if request.method == 'GET':
        return redirect(url_for('rehapp.patients'))

    invite_patient = InvitePatient(prefix="invite_patient")

    if invite_patient.validate_on_submit():
        print(invite_patient.add_angle_info)
        send_invite_email(invite_patient)

        flash('Invitation has been Sent. Ask Patient to Accept It.', "success")
        return redirect(url_for('rehapp.patients'))
    elif invite_patient.email.errors:
        flash(invite_patient.email.errors[0], "error")
    else:
        print(invite_patient.errors)
        flash('Unexpected Error during Invitation send process', "error")

    return redirect(url_for('rehapp.patients'))


# def send_reset_email(patient):
#     token = therapist.get_token()
#     msg = Message('Password Reset Request',
#                   sender='rehapp.project@gmail.com',
#                   recipients=[therapist.email])
#     msg.body = f'''To reset your password, visit the following link:
# {url_for('auth.login', pass_res_token=token, _external=True)}
#
# If you did not make this request then simply ignore this message.
# '''
#     mail.send(msg)


def send_invite_email(invite_patient):
    if invite_patient.add_angle_info.data:
        print(invite_patient.add_angle_info)
        token = Patient.get_params_token(therapist_id=current_user.id,
                                         patient_email=invite_patient.email.data,
                                         angle_from=invite_patient.angle_from.data,
                                         angle_to=invite_patient.angle_to.data,
                                         affected_side=invite_patient.affected_side.data,
                                         expires_sec=60 * 60 * 24 * 7)
    else:
        token = Patient.get_no_params_token(therapist_id=current_user.id,
                                            patient_email=invite_patient.email.data,
                                            expires_sec=60 * 60 * 24 * 7)

    msg = Message('Invitation Message',
                  sender='rehapp.project@gmail.com',
                  recipients=[invite_patient.email.data])

    if Patient.query.filter_by(email=invite_patient.email.data).first():
        msg.body = f'''Hi {invite_patient.email.data.split('@')[0]},
You have received an invitation from healthcare provider {current_user.first_name} {current_user.last_name} to join his/her Group on RehApp.{(chr(10) + "Note:" + chr(10) + invite_patient.note.data) if invite_patient.note.data else ""}

Please accept the invitation by clicking on the link below.
{url_for('auth.accept_invitation_handler', token=token, _external=True)}

If you do not wish to join this Group, simply ignore this message.

The RehApp team'''
    else:
        msg.body = f'''Hi {invite_patient.email.data.split('@')[0]},
You have received an invitation from healthcare provider {current_user.first_name} {current_user.last_name} to join his/her Group on RehApp.{(chr(10) + "Note:" + chr(10) + invite_patient.note.data) if invite_patient.note.data else ""}

By clicking on a link below you can create account and accept the invitation.
{url_for('auth.accept_invitation_handler', token=token, _external=True)}

If you do not wish to join this Group, simply ignore this message.

The RehApp team'''

    send_email(msg)


@rehapp.route('/patients/info_upload', methods=['GET', 'POST'])
@login_required
def patient_info_handler():
    if request.method == 'GET':
        return redirect(url_for('rehapp.patients'))

    print('Trying to accept p_id')
    patient_id = request.form['patient_id']
    if not patient_id:
        print('err')
        return jsonify(message="error", data="")
    else:
        print('ok: ' + patient_id)
        patient = Patient.query.get(patient_id)
        if patient:
            print(patient.birth_date)
            if patient.angle_limit_from is None or patient.angle_limit_to is None or patient.affected_side is None:
                return jsonify(message="ok", first_name=patient.first_name, last_name=patient.last_name,
                               email=patient.email, phone_num=patient.phone_num, sex=patient.sex,
                               birth_date=patient.birth_date, affected_side="Not Stated",
                               angle_limit_from="Not Stated", angle_limit_to="Not Stated")
            else:
                return jsonify(message="ok", first_name=patient.first_name, last_name=patient.last_name,
                               email=patient.email, phone_num=patient.phone_num, sex=patient.sex,
                               birth_date=patient.birth_date, affected_side=patient.affected_side,
                               angle_limit_from=patient.angle_limit_from, angle_limit_to=patient.angle_limit_to)

        else:
            flash('Something went wrong during Patien\'s Info uploading. Patient doesn\'t exist.', 'warning')
            return redirect(url_for('rehapp.patient'))


@rehapp.route('/patients/info_save', methods=['GET', 'POST'])
@login_required
def patient_info_save():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('rehapp.patients'))

    try:
        patient_id = request.form['patient_id']
        affected_side = request.form['affected_side']
        angle_limit_from = request.form['angle_limit_from']
        angle_limit_to = request.form['angle_limit_to']

        patient = Patient.query.get(patient_id)

        patient.affected_side = affected_side
        patient.angle_limit_from = angle_limit_from
        patient.angle_limit_to = angle_limit_to

        db.session.commit()
    except:
        return jsonify(message="error")

    return jsonify(message="ok", affected_side=patient.affected_side,
                   angle_limit_from=patient.angle_limit_from, angle_limit_to=patient.angle_limit_to)


@rehapp.route('/training', methods=['GET', 'POST'])
@login_required
def training():
    exercise_form = ExerciseForm(prefix='exercise_form')
    training_form = TrainingForm(prefix='training_form')

    patients_of_therapist = db.session.query(Patient) \
        .join(PatientOfTherapist, PatientOfTherapist.patient_id == Patient.id) \
        .filter(PatientOfTherapist.therapist_id == current_user.id) \
        .order_by(Patient.last_name.asc()).all()
    # Now forming the list of tuples for SelectField
    if patients_of_therapist:
        exercise_form.angle_from.data = patients_of_therapist[0].angle_limit_from
        exercise_form.angle_to.data = patients_of_therapist[0].angle_limit_to
        patients_names_list = \
            [(i.id, i.first_name + ' ' + i.last_name + ' (ID:' + str(i.id) + ')') for i in patients_of_therapist]
        training_form.patient_id.choices = patients_names_list

    return render_template('training.html', title='Training', training_form=training_form, today=date.today(),
                           exercise_form=exercise_form, patients_of_therapist=patients_of_therapist)


# ajax запрос на измение пациента
@rehapp.route('/training/change_patient', methods=['GET', 'POST'])
@login_required
def change_patient_handler():
    if request.method == 'GET':
        return redirect(url_for('rehapp.training'))

    patient_id = request.form['patient_id']
    if not patient_id:
        print('err')
        return jsonify(message="error", data="")
    else:
        print('ok: ' + patient_id)
        patient = Patient.query.get(patient_id)
        if patient:
            print()
            if patient.angle_limit_from is None or patient.angle_limit_to is None or patient.affected_side is None:
                return jsonify(message="ok", angle_limit_from="Not Stated", angle_limit_to="Not Stated")
            else:
                return jsonify(message="ok", angle_limit_from=patient.angle_limit_from,
                               angle_limit_to=patient.angle_limit_to)
        else:
            flash('Something went wrong during Patien\'s Info uploading. Patient doesn\'t exist.', 'warning')
            return redirect(url_for('rehapp.patient'))


@rehapp.route('/training/send_training', methods=['GET', 'POST'])
@login_required
def send_training_handler():
    if request.method == 'GET':
        return redirect(url_for('rehapp.training'))

    if request.is_json:
        request_json = request.get_json()
        print(request_json)
        print(request_json['exercises_array'][0]['order_in_training'])

        if request_json:
            training_info = request_json['training_info']

            # Если новая тренировка сегодня – делаем старую пропущенной с сегодняшней датой
            if training_info['training_form-training_date'] == date.today():
                old_trainings = db.session.query(Training)\
                    .filter(and_(Training.patient_id == training_info['training_form-patient_id'],
                                 Training.training_date <= training_info['training_form-training_date'],
                                 Training.execution_date == None)).all()

                if old_trainings:
                    for old_training in old_trainings:
                        old_training.execution_date = training_info['training_form-training_date']
                    db.session.commit()

            # Добавление новой тренировки
            assigned_by = current_user.first_name + ' ' + current_user.last_name[0] + '.'
            training_duration = timedelta()
            for exercise in request_json['exercises_array']:
                (m, s) = exercise['duration'].split(':')
                d = timedelta(minutes=int(m), seconds=int(s))
                training_duration += d

            print(training_duration)

            new_training = Training(patient_id=training_info['training_form-patient_id'],
                                    assigned_by=assigned_by,
                                    training_description=training_info['training_form-training_description'],
                                    training_date=training_info['training_form-training_date'],
                                    exercises_amount=len(request_json['exercises_array']),
                                    training_duration=training_duration
                                    )
            db.session.add(new_training)
            db.session.commit()
            db.session.refresh(new_training)

            training_id = new_training.id
            for exercise in request_json['exercises_array']:
                new_exercise = Exercise(training_id=training_id,
                                        order_in_training=exercise['order_in_training'],
                                        type=exercise['type'],
                                        speed=exercise['speed'],
                                        angle_limit_from=exercise['angle_limit_from'],
                                        angle_limit_to=exercise['angle_limit_to'],
                                        repetitions=exercise['repetitions'],
                                        spasms_stop_value=exercise['spasms_stop_value'],
                                        involvement_threshold=exercise['involvement'],
                                        repetition_timeout=exercise['repetition_timeout'],
                                        duration=exercise['duration']
                                        )
                db.session.add(new_exercise)
            db.session.commit()

            flash('Training has been Sent to the Patient successfully.', "success")
            return jsonify(message="ok", url=url_for('rehapp.training'))
        else:
            flash('Unexpected Error during Training send process.', "error")
            return jsonify(message="error", data='Received JSON is empty')

    else:
        flash('Unexpected Error during Training send process.', "error")
        return jsonify(message="error", data='Not JSON received')


@rehapp.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    patients_with_trainings = \
        db.session.query(Training).join(Patient, Training.patient_id == Patient.id) \
            .join(PatientOfTherapist, PatientOfTherapist.patient_id == Patient.id) \
            .filter(PatientOfTherapist.therapist_id == current_user.id).filter(Training.execution_date < datetime.now()) \
            .filter(Training.execution_date > datetime.now() - timedelta(weeks=4)) \
            .order_by(Training.execution_date.desc()).all()

    print(patients_with_trainings if patients_with_trainings else False)

    return render_template('schedule.html', title='Schedule', current_user=current_user,
                           patients_with_trainings=patients_with_trainings)
