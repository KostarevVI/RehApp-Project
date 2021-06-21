from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from website.models import *
from .__name__ import db, mail
from flask_login import login_user, login_required, logout_user, current_user
from .forms import InvitePatient, PatientInfoChange
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
    invite_patient = InvitePatient()
    patient_info_change = PatientInfoChange()


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

    invite_patient = InvitePatient()

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
You have received an invitation from healthcare provider {current_user.first_name} {current_user.last_name} to join his/her Group on RehApp.{(chr(10) + "Note:" + chr(10)+ invite_patient.note.data) if invite_patient.note.data else ""}

By clicking on a link below you can create account and accept the invitation.
{url_for('auth.accept_invitation_handler', token=token, _external=True)}

If you do not wish to join this Group, simply ignore this message.

The RehApp team'''

    send_email(msg)


@rehapp.route('/patients/info_upload', methods=['GET', 'POST'])
@login_required
def patient_info_handler():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('rehapp.dashboard'))
        else:
            return redirect(url_for('auth.login'))

    print('Trying to accept p_id')
    patient_id = request.form['patient_id']
    if not patient_id:
        print('err')
        return jsonify(message="error", data="")
    else:
        print('ok: ' + patient_id)
        patient = Patient.query.get(patient_id).first()

        return jsonify(message="ok", first_name=patient.first_name, last_name=patient.last_name,
                       email=patient.email, phone_num=patient.phone_num, sex=patient.sex,
                       birth_date=patient.birth_date, affected_side=patient.affected_side
                       # patient.angle_limit_tfrom
                       )
