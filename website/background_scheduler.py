from website.models import Training
from .__name__ import db
from sqlalchemy import *
from datetime import date
import time


def check_skipped_trainings():
    last_trainings = \
        db.session.query(Training.patient_id, func.max(Training.training_date).label('max_training_date'))\
        .filter(Training.training_date <= date.today()).group_by(Training.patient_id).subquery()

    skipped_trainings = db.session.query(Training)\
        .join(last_trainings, last_trainings.c.patient_id == Training.patient_id)\
        .filter(and_(Training.training_date < last_trainings.c.max_training_date, Training.execution_date == None))\
        .all()

    if skipped_trainings:
        print('Found skipped trainings')
        for skipped_training in skipped_trainings:
            patient_last_training = db.session.query(last_trainings).filter_by(patient_id=skipped_training.patient_id)\
                .first()
            skipped_training.execution_date = patient_last_training.max_training_date
            print(skipped_training.execution_date)

        db.session.commit()

    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
