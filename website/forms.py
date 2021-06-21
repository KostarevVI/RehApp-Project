from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField, PasswordField, BooleanField,
                     SubmitField, IntegerField, SelectField,
                     TextAreaField, DateField)
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from website.models import *


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired('Please enter Email Address.')])
    password = PasswordField('Password', validators=[InputRequired('Please enter Password.')])
    remember = BooleanField('Remember Me')
    submit1 = SubmitField('Login')


class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(message='First Name is too long.',
                                                                               max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(message='Last Name is too long.',
                                                                             max=30)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Email Address does Not Exists.',
                                                                    check_deliverability='True')])
    phone_num = StringField('Phone Number', validators=[InputRequired(), Length(message='Phone Number is too long.',
                                                                                 max=20)])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(message='Password must be between 8 and 80 characters long.'
                                                            , min=8
                                                            , max=80),
                                                     EqualTo('conf', message='Passwords must match.')])
    conf = PasswordField('Confirm Password', validators=[InputRequired()])
    submit2 = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Therapist.query.filter_by(email=email.data, is_verified=True).first()
        if user:
            raise ValidationError('Account with this Email already Exists. Please Sign Up with another Email.')


class RecaptchaForm(FlaskForm):
    recaptcha = RecaptchaField()
    recaptcha_error = StringField('Error handler')


class PasswordReset(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit3 = SubmitField('Request Password Reset')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(message='Password must be between 8 and 80 characters long.'
                                                            , min=8
                                                            , max=80),
                                                     EqualTo('conf', message='Passwords must match.')])
    conf = PasswordField('Confirm Password', validators=[InputRequired()])
    submit4 = SubmitField('Submit')


class InvitePatient(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Email Address does Not Exists.',
                                                                    check_deliverability='True')])
    add_angle_info = BooleanField('Add Angle Info')
    angle_from = IntegerField('Angle From')
    angle_to = IntegerField('Angle To')
    affected_side = SelectField("Affected side", choices=[('left', "Left"), ('right', 'Right'), ('both', 'Both')],
                                default=1)
    note = TextAreaField('Note', render_kw={"rows": 3})
    submit5 = SubmitField('Send Invitation')


class PatientsSignUp(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(message='First Name is too long.',
                                                                               max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(message='Last Name is too long.',
                                                                             max=30)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Email Address does Not Exists.',
                                                                    check_deliverability='True')])
    phone_num = StringField('Phone Number', validators=[InputRequired(), Length(message='Phone Number is too long.',
                                                                                max=20)])
    sex = SelectField("Sex", choices=[('male', "Male"), ('female', 'Female'), ('custom', 'Custom')],
                      default=1)
    birth_date = DateField('Birth Date', format='%Y-%m-%d', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(message='Password must be between 8 and 80 characters long.'
                                                            , min=8
                                                            , max=80),
                                                     EqualTo('conf', message='Passwords must match.')])
    conf = PasswordField('Confirm Password', validators=[InputRequired()])
    submit6 = SubmitField('Sign Up')

    # спрятанные поля
    therapist_id = StringField('Therapist Id')
    angle_from = StringField('Angle From')
    angle_to = StringField('Angle To')
    affected_side = StringField('Affected Side')

    def validate_email(self, email):
        patient = Patient.query.filter_by(email=email.data, is_verified=True).first()
        if patient:
            raise ValidationError('Account with this Email already Exists. Please Sign Up with another Email.')

    def validate_therapist_id(self, therapist_id):
        therapist = Therapist.query.filter_by(id=therapist_id.data, is_verified=True).first()
        if not therapist:
            raise ValidationError('Account that invited you does not exist anymore. Please contact your Therapist.')


class PatientInfoChange(FlaskForm):
    add_angle_info = BooleanField('Add Angle Info')
    angle_from = IntegerField('Angle From')
    angle_to = IntegerField('Angle To')
    affected_side = SelectField("Affected side", choices=[('left', "Left"), ('right', 'Right'), ('both', 'Both')],
                                default=1)
    submit7 = SubmitField('Save')


