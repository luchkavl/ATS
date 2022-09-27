import uuid

from sqlalchemy.orm import Session, joinedload

from ats import enums
import database.models as db_models


def fetch_vacancy_by_name(db: Session, vacancy_name: enums.Vacancies):
    return db.query(db_models.Vacancy).filter(db_models.Vacancy.name == vacancy_name).one()


def fetch_all_full_info_candidates(db: Session):
    return db.query(db_models.Candidate).options(
        joinedload(db_models.Candidate.vacancies), joinedload(db_models.Candidate.feedbacks))\
        .all()


def fetch_full_info_candidates_by_status(db: Session, status: enums.Statuses):
    return db.query(db_models.Candidate).filter(db_models.Candidate.status == status).options(
        joinedload(db_models.Candidate.vacancies), joinedload(db_models.Candidate.feedbacks))\
        .all()


def fetch_full_info_candidate_by_id(db: Session, candidate_id: uuid.UUID):
    return db.query(db_models.Candidate).filter(db_models.Candidate.id == candidate_id).options(
        joinedload(db_models.Candidate.vacancies), joinedload(db_models.Candidate.feedbacks)).\
        one_or_none()


def fetch_base_info_candidate_by_id(db: Session, candidate_id: uuid.UUID):
    return db.query(db_models.Candidate).filter(db_models.Candidate.id == candidate_id).one_or_none()


def fetch_all_candidates_by_vacancy_status(db: Session, vacancy: enums.Vacancies, status: enums.Statuses):
    return db.query(db_models.Candidate).\
        filter(db_models.Candidate.vacancies.any(name=vacancy)).filter(db_models.Candidate.status == status)\
        .all()


def fetch_all_candidates_from_vacancy(db: Session, vacancy: enums.Vacancies):
    return db.query(db_models.Candidate).filter(db_models.Candidate.vacancies.any(name=vacancy)).all()