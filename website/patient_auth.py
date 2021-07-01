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

    try:
        token = request.headers['authorization']
    except:
        return Response("{'message':'User token is required.'}", status=400, mimetype='application/json')

    patient = Patient.verify_token(token)

    if patient:
        training = db.session.query(Training).filter(and_(Training.patient_id == patient.id,
                                                      Training.execution_date == None,
                                                      Training.training_date <= date.today())).first()
        if training:
            exercises_in_training = db.session.query(Exercise).filter(Exercise.training_id == training.id).all()

            if exercises_in_training:
                training_schema = TrainingSchema()
                exercise_schema = ExerciseSchema(many=True)
                print(training_schema.dump(training))

                training_output = json.dumps(training_schema.dump(training))
                exercises_output = json.dumps(exercise_schema.dump(exercises_in_training))

                return Response('{"data":{"training":' + '"' + training_output + '", "exercises":' + exercises_output +
                                '}, "status":200}', status=200, mimetype='application/json')
            else:
                return Response("{'message':'Unexpected error. Empty training.'}", status=406,
                                mimetype='application/json')
        else:
            return Response("{'message':'There is no new trainings for you.'}", status=200, mimetype='application/json')
    else:
        return Response("{'message':'You are not authorized. Please Login again.'}", status=401, mimetype='application/json')
