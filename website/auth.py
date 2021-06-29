from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from website.models import *
from .__name__ import db, mail
from flask_login import login_user, login_required, logout_user, current_user
from .forms import (LoginForm, SignUpForm, PasswordReset,
                    PasswordResetForm, RecaptchaForm, PatientsSignUp)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from .async_email import send_email
import datetime


auth = Blueprint('auth', __name__)


@auth.route('/', defaults={'pass_res_token': None}, methods=['GET', 'POST'])
@auth.route('/<pass_res_token>', methods=['GET', 'POST'])
def login(pass_res_token):
    if current_user.is_authenticated:
        return redirect(url_for('rehapp.dashboard'))

    login_form = LoginForm(prefix="login_form")
    sign_up_form = SignUpForm(prefix="sign_up_form")
    pass_res = PasswordReset(prefix="pass_res")
    pass_res_form = PasswordResetForm(prefix="pass_res_form")
    recaptcha_form = RecaptchaForm(prefix="recaptcha_form")

    if pass_res_token and pass_res_token != '':
        therapist = Therapist.verify_token(pass_res_token)
        if therapist is None:
            flash('Link that you used is Invalid or Expired. Please try to send Request again.', 'error')
            return redirect(url_for('auth.login'))

        if pass_res_form.validate_on_submit():
            pass_hash = generate_password_hash(pass_res_form.password.data)
            therapist.password = pass_hash
            db.session.commit()
            flash('Password has been Changed Successfully! You are now able to Log In.', 'success')
            return redirect(url_for('auth.login'))
        elif pass_res_form.password.errors:
            flash(pass_res_form.password.errors[0], "error")
        else:
            flash('Something went wrong during Password Change Procedure. Please try again.', 'error')

        return render_template('login.html', current_user=current_user, login_form=login_form, sign_up_form=sign_up_form,
                               pass_res=pass_res, pass_res_form=pass_res_form, recaptcha_form=recaptcha_form,
                               is_pass_res=True)

    return render_template('login.html', current_user=current_user, login_form=login_form, sign_up_form=sign_up_form, # login.html
                           pass_res=pass_res, pass_res_form=pass_res_form, recaptcha_form=recaptcha_form,
                           is_pass_res=False)


@auth.route('/login', methods=['GET', 'POST'])
def login_handler():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('rehapp.dashboard'))
        else:
            return redirect(url_for('auth.login'))

    login_form = LoginForm(prefix="login_form")

    if login_form.validate_on_submit():

        therapist = Therapist.query.filter_by(email=login_form.email.data.lower().strip()).first()

        if therapist and check_password_hash(therapist.password, login_form.password.data):
            if therapist.is_verified:
                login_user(therapist, remember=login_form.remember.data)
                return redirect(url_for('rehapp.dashboard'))
            else:
                flash('Your Account is not Verified. Please Check your Email for Confirmation Link. Sign Up again if it\'s invalid.', category='warning')  # ????????????????????????????
                return redirect(url_for('auth.login'))
        else:
            flash("Invalid Email and Password combination.", "error")

    return redirect(url_for('auth.login'))

    # return render_template("login.html", user=current_user, login_form=login_form, sign_up_form=sign_up_form)


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up_handler():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('rehapp.dashboard'))
        else:
            return redirect(url_for('auth.login'))

    sign_up_form = SignUpForm(prefix="sign_up_form")

    print('Trying to validate')
    print(sign_up_form.errors)

    if sign_up_form.validate_on_submit():
        print('Okkkkkkk')
        therapist_verify = Therapist.query.filter_by(email=sign_up_form.email.data, is_verified=False).first()
        if therapist_verify:
            send_verify_email(therapist_verify)

            flash("Account already Exists but not Verified. Confirmation Link was Sent Again. Please Check your Email.", "warning")

            return redirect(url_for('auth.login'))

        else:
            pass_hash = generate_password_hash(sign_up_form.password.data)
            phone_num = '+' + str(sign_up_form.phone_num.data).translate(str.maketrans('', '', '-+. '))

            new_therapist = Therapist(password=pass_hash,
                                      first_name=sign_up_form.first_name.data,
                                      last_name=sign_up_form.last_name.data,
                                      email=sign_up_form.email.data,
                                      phone_num=phone_num
                                      )
            db.session.add(new_therapist)
            db.session.commit()
            db.session.refresh(new_therapist)

            send_verify_email(new_therapist)

            flash("Account Created. Check your Email from Confirmation Link to Verify your Account.", "success")

            return redirect(url_for('auth.login'))

    elif sign_up_form.email.errors:
        print('Email: ' + sign_up_form.email.errors[0])
        flash(sign_up_form.email.errors[0], "error")
    elif sign_up_form.password.errors:
        print('Password:' + sign_up_form.password.errors[0])
        flash(sign_up_form.password.errors[0], "error")
    else:
        print('what?')

    print(sign_up_form.errors)

    return redirect(url_for('auth.login'))


@auth.route('/recaptcha_verify', methods=['GET', 'POST'])
def recaptcha_verify_handler():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('rehapp.dashboard'))
        else:
            return redirect(url_for('auth.login'))

    sign_up_form = SignUpForm(prefix="sign_up_form")
    recaptcha_form = RecaptchaForm(prefix="recaptcha_form")

    print('Trying to validate')
    if not recaptcha_form.recaptcha.validate(form=sign_up_form):
        print('Val err')
        return jsonify(message="error", data=recaptcha_form.errors)
    else:
        print('Val ok')

    print(recaptcha_form.errors)
    return jsonify(message="ok", data=recaptcha_form.errors)


@auth.route('/pass_res', methods=['GET', 'POST'])
def pass_res_handler():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('rehapp.dashboard'))
        else:
            return redirect(url_for('auth.login'))

    pass_res = PasswordReset(prefix="pass_res")

    if pass_res.validate_on_submit():
        therapist = Therapist.query.filter_by(email=pass_res.email.data).first()
        print(therapist.id)
        if therapist and therapist.is_verified:
            send_reset_email(therapist)
        flash('Password Reset Link has been Sent to your Email If your Account Exists and is Verified.', "success")
        return redirect(url_for('auth.login'))
    elif pass_res.email.errors:
        flash(pass_res.email.errors[0], "error")
    else:
        flash('Unexpected Error during Password Resetting send request', "error")

    return redirect(url_for('auth.login'))


@auth.route('/verify_account/<token>', methods=['GET', 'POST'])
def verify_account_handler(token):
    if current_user.is_authenticated:
        return redirect(url_for('rehapp.dashboard'))

    therapist = Therapist.verify_token(token)
    print(therapist.id)
    if therapist is None:
        flash('Link that you used is Invalid or Expired. Please Sign Up again to get a new one.', 'error')
        return redirect(url_for('auth.login'))
    else:
        therapist.is_verified = True
        db.session.commit()

        flash('Account Verified. You can Log In now.', 'success')
        return redirect(url_for('auth.login'))


def send_reset_email(therapist):
    token = therapist.get_token()
    msg = Message('Password Reset Request',
                  sender='rehapp.project@gmail.com',
                  recipients=[therapist.email])
    msg.body = f'''Hi {therapist.email.split('@')[0]},
To reset your password, visit the following link:
{url_for('auth.login', pass_res_token=token, _external=True)}

If you did not make this request then simply ignore this message.

The RehApp team
'''
    send_email(msg)


def send_verify_email(therapist):
    token = therapist.get_token(expires_sec=60*60*24*7)
    msg = Message('Account Confirmation',
                  sender='rehapp.project@gmail.com',
                  recipients=[therapist.email])
    msg.body = f'''Hi {therapist.email.split('@')[0]},
To confirm your account, visit the following link:
{url_for('auth.verify_account_handler', token=token, _external=True)}

If you did not make this request then simply ignore this message.

The RehApp team
'''
    send_email(msg)


@auth.route('/sign_out')
@login_required
def sign_out_handler():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/accept-invitation/<token>', methods=['GET', 'POST'])
def accept_invitation_handler(token):
    patients_sign_up = PatientsSignUp()

    # token_info = [therapist_id, patient_email, angle_from, angle_to, affected_side]
    token_info = Patient.verify_params_token(token)
    if token_info is not None:
        patient = Patient.query.filter_by(email=token_info[1]).first()
        if patient is None:
            print('Val Pat reg' + str(token_info))
            patients_sign_up_params = PatientsSignUp(therapist_id=token_info[0],
                                                     email=token_info[1],
                                                     angle_from=token_info[2],
                                                     angle_to=token_info[3],
                                                     affected_side=token_info[4])
            patients_sign_up_params.therapist_id.data = token_info[0]

            return render_template('patients_sign_up.html', patients_sign_up=patients_sign_up_params,
                                   today=datetime.date.today(), message=None)
        else:
            if (PatientOfTherapist.query
                    .filter(PatientOfTherapist.therapist_id == token_info[0])
                    .filter(PatientOfTherapist.patient_id == patient.id)
                    .filter(PatientOfTherapist.therapy_end_date == None).first()):
                return render_template('patients_sign_up.html', patients_sign_up=patients_sign_up,
                                       today=datetime.date.today(), message='You are already a member of this group.')
            else:
                active_therapies = PatientOfTherapist.query \
                    .filter(PatientOfTherapist.patient_id == patient.id) \
                    .filter(PatientOfTherapist.therapy_end_date == None).all()
                print(active_therapies)
                for therapy in active_therapies:
                    print(therapy)
                    therapy.therapy_end_date = datetime.datetime.now()

                patient.angle_limit_from = token_info[2]
                patient.angle_limit_to = token_info[3]
                patient.affected_side = token_info[4]
                patient.is_verified = True
                patient.update_date = datetime.datetime.now()

                patient_of_therapist = PatientOfTherapist(therapist_id=token_info[0], patient_id=patient.id)
                db.session.add(patient_of_therapist)
                db.session.commit()
                return render_template('patients_sign_up.html',
                                       patients_sign_up=patients_sign_up,
                                       today=datetime.date.today(),
                                       message='Invitation Accepted. Now you are a member of this group.')

    # token_info = [therapist_id, patient_email]
    token_info = Patient.verify_no_params_token(token)
    if token_info is not None:
        patient = Patient.query.filter_by(email=token_info[1]).first()
        if patient is None:
            print('no Val Pat reg ' + str(token_info))
            patients_sign_up_no_params = PatientsSignUp(therapist_id=token_info[0],
                                                        email=token_info[1])

            return render_template('patients_sign_up.html', patients_sign_up=patients_sign_up_no_params,
                                   today=datetime.date.today(), message=None)
        else:
            if (PatientOfTherapist.query
                    .filter(PatientOfTherapist.therapist_id == token_info[0])
                    .filter(PatientOfTherapist.patient_id == patient.id)
                    .filter(PatientOfTherapist.therapy_end_date == None).first()):
                return render_template('patients_sign_up.html', patients_sign_up=patients_sign_up,
                                       today=datetime.date.today(), message='You are already a member of this group.')
            else:
                active_therapies = PatientOfTherapist.query\
                                    .filter(PatientOfTherapist.patient_id == patient.id)\
                                    .filter(PatientOfTherapist.therapy_end_date == None).all()

                for therapy in active_therapies:
                    therapy.therapy_end_date = datetime.datetime.now()

                patient.is_verified = True
                patient.update_date = datetime.datetime.now()

                patient_of_therapist = PatientOfTherapist(therapist_id=token_info[0], patient_id=patient.id)
                db.session.add(patient_of_therapist)
                db.session.commit()
                return render_template('patients_sign_up.html',
                                       patients_sign_up=patients_sign_up,
                                       today=datetime.date.today(),
                                       message='Invitation accepted. Now you are a member of this group.')

    return render_template('patients_sign_up.html',
                           patients_sign_up=patients_sign_up,
                           today=datetime.date.today(),
                           message='Invalid or Expired URL.')


@auth.route('/patients_sign_up', methods=['GET', 'POST'])
def patients_sign_up_handler():
    patients_sign_up = PatientsSignUp()
    print(patients_sign_up.therapist_id.data + ' ' + patients_sign_up.angle_from.data + ' ' + patients_sign_up.password.data)
    if patients_sign_up.validate_on_submit():
        pass_hash = generate_password_hash(patients_sign_up.password.data)
        phone_num = '+' + str(patients_sign_up.phone_num.data).translate(str.maketrans('', '', '-+. '))

        if (patients_sign_up.affected_side.data == ''
                or patients_sign_up.angle_from.data == ''
                or patients_sign_up.angle_to.data == ''):
            new_patient = Patient(password=pass_hash,
                                  first_name=patients_sign_up.first_name.data,
                                  last_name=patients_sign_up.last_name.data,
                                  email=patients_sign_up.email.data,
                                  phone_num=phone_num,
                                  sex=patients_sign_up.sex.data,
                                  birth_date=patients_sign_up.birth_date.data,
                                  is_verified=True
                                  )
        else:
            new_patient = Patient(password=pass_hash,
                                  first_name=patients_sign_up.first_name.data,
                                  last_name=patients_sign_up.last_name.data,
                                  email=patients_sign_up.email.data,
                                  phone_num=phone_num,
                                  sex=patients_sign_up.sex.data,
                                  birth_date=patients_sign_up.birth_date.data,
                                  angle_limit_from=patients_sign_up.angle_from.data,
                                  angle_limit_to=patients_sign_up.angle_to.data,
                                  affected_side=patients_sign_up.affected_side.data,
                                  is_verified=True
                                  )

        db.session.add(new_patient)
        db.session.commit()
        db.session.refresh(new_patient)

        new_patient_of_therapist = PatientOfTherapist(therapist_id=patients_sign_up.therapist_id.data,
                                                      patient_id=new_patient.id)
        db.session.add(new_patient_of_therapist)
        db.session.commit()

        return render_template('patients_sign_up.html',
                               patients_sign_up=patients_sign_up,
                               today=datetime.date.today(),
                               message='Account Created Successfully. Now you are a member of this group.'
                                       ' Log in with mobile App to start your trainings.')
    else:
        return render_template('patients_sign_up.html',
                               patients_sign_up=patients_sign_up,
                               today=datetime.date.today(),
                               message='Something went wrong during account creation.')



# @auth.route('/register', method=['POST'])
# def register():
#     user = User.query.filter_by(id=id).first_or_404()
#     form = ProfileEditForm(user.email)
#     if form.validate_on_submit():
#         user.email = form.email.data
#         db.session.commit()
#         return jsonify(status='ok')
#     elif request.method == 'GET':
#         form.email.data = user.email
#     else:
#         data = json.dumps(form.errors, ensure_ascii=False)
#         return jsonify(data)
#     return render_template('_form_edit.html', title="Редактирование пользователя", form=form)


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#
#         user = UserDatum.query.filter_by(email=email.lower()).first()
#         if user:
#             if user.password == password:
#                 flash('Logged in successfully!', category='success')
#                 login_user(user, remember=True)
#                 return redirect(url_for('game_menu.select_person'))
#             else:
#                 flash('Incorrect password, try again.', category='error')
#         else:
#             flash('Email does not exist.', category='error')
#
#     return render_template("login.html", user=current_user)
#
#
# @auth.route('/logout')
# @login_required
# def logout():
#     logout_clear()
#     logout_user()
#     return redirect(url_for('auth.login'))
#
#
# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         nickname = request.form.get('nickname')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')
#
#         user = UserDatum.query.filter_by(email=email).first()
#         if user:
#             flash('Email already exists.', category='error')
#         elif len(email) < 4:
#             flash('Email must be greater than 3 characters.', category='error')
#         elif len(nickname) < 2:
#             flash('Nickname must be greater than 1 character.', category='error')
#         elif password1 != password2:
#             flash('Passwords don\'t match.', category='error')
#         elif len(password1) < 7:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
#             new_user = UserDatum(email=email, nickname=nickname, password=password1)
#             db.session.add(new_user)
#             db.session.commit()
#             login_user(new_user, remember=True)
#             flash('Account created!', category='success')
#             return redirect(url_for('auth.login'))
#
#     return render_template("sign_up.html", user=current_user)
