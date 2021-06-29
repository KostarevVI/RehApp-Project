from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, Response, json
from website.models import *
from .__name__ import db, mail, csrf
from flask_login import login_user, login_required, logout_user, current_user
from .forms import (LoginForm, SignUpForm, PasswordReset,
                    PasswordResetForm, RecaptchaForm, PatientsSignUp)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from .async_email import send_email
from _datetime import date
from sqlalchemy import *


patient_auth = Blueprint('patient_auth', __name__)


@patient_auth.route('/patient_login', methods=['GET', 'POST'])
@csrf.exempt
def patient_login_handler():
    if request.method == 'GET':
        return 'Go away!'

    patient_json = request.get_json()
    email = patient_json['email']
    password = patient_json['password']

    patient = Patient.query.filter_by(email=email.lower().strip()).first()

    if patient and check_password_hash(patient.password, password):
        if patient.is_verified:
            token = patient.get_token()
            return Response('{"data":{"token":' + '"' + token + '"}, "status":200}', status=200, mimetype='application/json')
        else:
            return Response("{'message':'You are not verified'}", status=403, mimetype='application/json')

    else:
        return Response("{'message':'Login and password pair is incorrect'}", status=400, mimetype='application/json')


@patient_auth.route('/get_patient_training', methods=['GET', 'POST'])
@csrf.exempt
def patient_training_handler():
    if request.method == 'POST':
        return 'Go away!'

    token = request.headers['authorization']
    print(token)

    patient = Patient.verify_token(token)
    print(patient.id)

    if patient:
        training = db.session.query(Training).filter(and_(Training.patient_id == patient.id,
                                                      Training.execution_date == None,
                                                      Training.training_date <= date.today())).first()

        if training:
            exercises_in_training = db.session.query(Exercise).filter(Exercise.training_id == training.id).all()

            training_json = json.dumps(training.serialize())
            exercises_in_training_json = jsonify(exersises=Exercise.serialize_list(exercises_in_training))

            return Response('{"data":{"training":' + '"' + training_json + '", "exercises":' + exercises_in_training_json + '}, "status":200}', status=200, mimetype='application/json')
        else:
            return Response("{'message':'You are not verified'}", status=403, mimetype='application/json')
    else:
        return Response("{'message':'Login and password pair is incorrect'}", status=400, mimetype='application/json')
