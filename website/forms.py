from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField, PasswordField, BooleanField,
                     SubmitField, IntegerField, SelectField,
                     TextAreaField, DateField, RadioField,
                     TimeField)
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError, NumberRange
from website.models import *


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired('Please enter Email Address.')])
    password = PasswordField('Password', validators=[InputRequired('Please enter Password.')])
    remember = BooleanField('Remember Me')
    submit1 = SubmitField('Login')


class SignUpForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[InputRequired(),
                                         Length(message='First Name is too long.',
                                                max=30)])
    last_name = StringField('Last Name',
                            validators=[InputRequired(),
                                        Length(message='Last Name is too long.',
                                               max=30)])
    email = StringField('Email',
                        validators=[InputRequired(),
                                    Email(message='Email Address does Not Exists.',
                                          check_deliverability='True')])
    phone_num = StringField('Phone Number',
                            validators=[InputRequired(),
                                        Length(message='Phone Number is too long.',
                                               max=20)])
    password = \
        PasswordField('Password',
                      validators=[InputRequired(),
                                  Length(message='Password must be between 8 and 80 characters long.',
                                         min=8,
                                         max=80),
                                  EqualTo('conf', message='Passwords must match.')])
    conf = PasswordField('Confirm Password', validators=[InputRequired()])
    submit2 = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Therapist.query.filter_by(email=email.data, is_verified=True).first()
        if user:
            raise ValidationError('Account with this Email already Exists. '
                                  'Please Sign Up with another Email.')


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
                                default='left')
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
                      default='male')
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
                                default='left')
    submit7 = SubmitField('Save')


class TrainingForm(FlaskForm):
    patient_id = SelectField('Select Patient', choices=[], coerce=int, validators=[InputRequired()])
    training_description = TextAreaField("Description")
    training_date = DateField('Training Date', format='%Y-%m-%d', validators=[InputRequired()])
    submit8 = SubmitField('Send Training')


class ExerciseForm(FlaskForm):
    type = RadioField('Training Type', choices=[('passive', 'Passive'), ('active', 'Active')], default='passive')
    involvement = SelectField('Select Involvement', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                             ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
                                                             ('9', '9'), ('10', '10')], default='1')
    timeout = SelectField('', choices=[('00:00:05', '5 sec.'), ('00:00:10', '10 sec.'), ('00:00:15', '15 sec.'),
                                       ('00:00:20', '20 sec.'), ('00:00:25', '25 sec.'), ('00:00:30', '30 sec.')],
                          default='00:00:15')
    speed = SelectField('Select Speed', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
                                                 ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')],
                        default='1', validators=[InputRequired()])
    angle_from = IntegerField('Angle From', validators=[InputRequired(), NumberRange(min=0, max=135)])
    angle_to = IntegerField('Angle To', validators=[InputRequired(), NumberRange(min=0, max=135)])
    repetitions = IntegerField('Repetitions', validators=[InputRequired(), NumberRange(min=1, max=50)])
    spasms_stop_value = SelectField('Spasms Stop Value', choices=[('0', 'None (set Angle)'), ('1', '1'), ('2', '2'),
                                                                  ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
                                                                  ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
    duration = TimeField('Duration', format='%M:%S', validators=[InputRequired()])
    submit9 = SubmitField('Add Exercise')
