# coding: utf-8
from sqlalchemy import ARRAY, Boolean, CheckConstraint, Column, Date, DateTime, Enum, ForeignKey, Integer, SmallInteger, \
    String, Table, Text, Time, text, UniqueConstraint
from sqlalchemy.orm import relationship
from .__name__ import db, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer
from sqlalchemy.inspection import inspect

metadata = db.metadata


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class Patient(db.Model):
    __tablename__ = 'patient'
    __table_args__ = (
        CheckConstraint('(angle_limit_from <= 135) AND (angle_limit_to >= angle_limit_from)'),
        CheckConstraint('(angle_limit_from >= 0) AND (angle_limit_from <= angle_limit_to)'),
        CheckConstraint("(email)::text <> ''::text"),
        CheckConstraint("(first_name)::text <> ''::text"),
        CheckConstraint("(last_name)::text <> ''::text"),
        CheckConstraint("(password)::text <> ''::text"),
        CheckConstraint("(phone_num)::text <> ''::text")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('patient_id_seq'::regclass)"))
    password = Column(String(255), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone_num = Column(String(20), nullable=False)
    sex = Column(Enum('male', 'female', 'custom', name='sex_type'), nullable=False)
    birth_date = Column(Date, nullable=False)
    update_date = Column(DateTime, nullable=False, server_default=text("now()"))
    affected_side = Column(Enum('left', 'right', 'both', name='affected_type'))
    angle_limit_from = Column(SmallInteger)
    angle_limit_to = Column(SmallInteger)
    is_verified = Column(Boolean, nullable=False, server_default=text("false"))

    def get_token(self, expires_sec=60 * 60 * 24):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'patient_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])

        try:
            patient_id = s.loads(token)['patient_id']
        except:
            return None
        return Patient.query.get(patient_id)

    @staticmethod
    def get_params_token(therapist_id, patient_email, angle_from, angle_to, affected_side, expires_sec=60 * 60 * 24):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'therapist_id': therapist_id,
                        'patient_email': patient_email,
                        'angle_from': angle_from,
                        'angle_to': angle_to,
                        'affected_side': affected_side}).decode('utf-8')

    @staticmethod
    def verify_params_token(token):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])

        try:
            therapist_id = s.loads(token)['therapist_id']
            patient_email = s.loads(token)['patient_email']
            angle_from = s.loads(token)['angle_from']
            angle_to = s.loads(token)['angle_to']
            affected_side = s.loads(token)['affected_side']
        except:
            return None
        return [therapist_id, patient_email, angle_from, angle_to, affected_side]

    @staticmethod
    def get_no_params_token(therapist_id, patient_email, expires_sec=60 * 60 * 24):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'therapist_id': therapist_id,
                        'patient_email': patient_email}).decode('utf-8')

    @staticmethod
    def verify_no_params_token(token):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])

        try:
            therapist_id = s.loads(token)['therapist_id']
            patient_email = s.loads(token)['patient_email']
        except:
            return None
        return [therapist_id, patient_email]


class Therapist(db.Model, UserMixin):
    __tablename__ = 'therapist'
    __table_args__ = (
        CheckConstraint("(email)::text <> ''::text"),
        CheckConstraint("(first_name)::text <> ''::text"),
        CheckConstraint("(last_name)::text <> ''::text"),
        CheckConstraint("(password)::text <> ''::text"),
        CheckConstraint("(phone_num)::text <> ''::text")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('therapist_id_seq'::regclass)"))
    password = Column(String(255), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone_num = Column(String(20), nullable=False)
    update_date = Column(DateTime, nullable=False, server_default=text("now()"))
    is_verified = Column(Boolean, nullable=False, server_default=text("false"))

    def get_token(self, expires_sec=60 * 60 * 24):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'therapist_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])

        try:
            therapist_id = s.loads(token)['therapist_id']
        except:
            return None
        return Therapist.query.get(therapist_id)


class PatientOfTherapist(db.Model):
    __tablename__ = 'patient_of_therapist'
    __table_args__ = (
        UniqueConstraint('therapist_id', 'patient_id', 'therapy_start_date'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('patient_of_therapist_id_seq'::regclass)"))
    therapist_id = Column(ForeignKey('therapist.id', ondelete='SET NULL'))
    patient_id = Column(ForeignKey('patient.id', ondelete='CASCADE'))
    therapy_start_date = Column(DateTime, nullable=False, server_default=text("now()"))
    therapy_end_date = Column(DateTime)

    patient = relationship('Patient')
    therapist = relationship('Therapist')


class Training(db.Model, Serializer):
    __tablename__ = 'training'
    __table_args__ = (
        CheckConstraint("(assigned_by)::text <> ''::text"),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('training_id_seq'::regclass)"))
    patient_id = Column(ForeignKey('patient.id', ondelete='CASCADE'))
    assigned_by = Column(String(60), nullable=False)
    training_description = Column(Text)
    training_date = Column(Date, nullable=False)
    exercises_amount = Column(Integer, nullable=False)
    training_duration = Column(Time, nullable=False)
    execution_date = Column(Date)
    exercise_done_count = Column(Integer)
    stop_reason = Column(Enum('end', 'spasms', 'tired', 'pain', 'unstated', name='reason_type'))
    spasms_total = Column(Integer)

    patient = relationship('Patient')

    def serialize(self):
        d = Serializer.serialize(self)
        del d['patient_id']
        return d


class Exercise(db.Model, Serializer):
    __tablename__ = 'exercise'
    __table_args__ = (
        CheckConstraint('(involvement_threshold > 0) AND (involvement_threshold <= 10)'),
        CheckConstraint('(repetitions > 0) AND (repetitions <= 50)'),
        CheckConstraint('(spasms_stop_value <= 10) AND (spasms_stop_value >= 0)'),
        CheckConstraint('(speed > 0) AND (speed <= 10)')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('exercise_id_seq'::regclass)"))
    training_id = Column(ForeignKey('training.id', ondelete='CASCADE'))
    order_in_training = Column(Integer, nullable=False)
    type = Column(Enum('passive', 'active', name='exercise_type'), nullable=False)
    speed = Column(SmallInteger, nullable=False)
    angle_limit_from = Column(SmallInteger, nullable=False)
    angle_limit_to = Column(SmallInteger, nullable=False)
    repetitions = Column(Integer, nullable=False)
    spasms_stop_value = Column(Integer, nullable=False, server_default=text("0"))
    involvement_threshold = Column(SmallInteger)
    repetition_timeout = Column(Time)
    duration = Column(Time)
    spasms_count = Column(Integer)

    training = relationship('Training')

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class ExerciseGraph(db.Model):
    __tablename__ = 'exercise_graph'

    id = Column(Integer, primary_key=True, server_default=text("nextval('exercise_graph_id_seq'::regclass)"))
    exercise_id = Column(ForeignKey('exercise.id', ondelete='CASCADE'))
    graph_type = Column(Enum('involvement_biceps', 'involvement_triceps', name='graph_type'), nullable=False)
    plot_x = Column(ARRAY(String(length=30)), nullable=False)
    plot_y = Column(ARRAY(String(length=30)), nullable=False)

    exercise = relationship('Exercise')
