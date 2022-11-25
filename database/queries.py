import uuid
from typing import List
from sqlalchemy.orm import Session, joinedload

from ats import enums
from database.models import VacancyModel, CandidateModel


def fetch_vacancy_by_name(db: Session, vacancy_name: enums.Vacancies) -> VacancyModel:
    return db.query(VacancyModel).filter(VacancyModel.name == vacancy_name).one()


def fetch_all_full_info_candidates(db: Session) -> List[CandidateModel]:
    return db.query(CandidateModel).options(
        joinedload(CandidateModel.vacancies), joinedload(CandidateModel.feedbacks)) \
        .all()


def fetch_full_info_candidates_by_status(db: Session, status: enums.Statuses) -> List[CandidateModel]:
    return db.query(CandidateModel).filter(CandidateModel.status == status).options(
        joinedload(CandidateModel.vacancies), joinedload(CandidateModel.feedbacks)) \
        .all()


def fetch_full_info_candidate_by_id(db: Session, candidate_id: uuid.UUID) -> CandidateModel | None:
    return db.query(CandidateModel).filter(CandidateModel.candidate_id == candidate_id).options(
        joinedload(CandidateModel.vacancies), joinedload(CandidateModel.feedbacks)). \
        one_or_none()


def fetch_base_info_candidate_by_id(db: Session, candidate_id: uuid.UUID) -> CandidateModel | None:
    return db.query(CandidateModel).filter(CandidateModel.candidate_id == candidate_id).one_or_none()


def fetch_all_candidates_by_vacancy_status(
        db: Session, vacancy: enums.Vacancies, status: enums.Statuses) -> List[CandidateModel]:
    return db.query(CandidateModel). \
        filter(CandidateModel.vacancies.any(name=vacancy)).filter(CandidateModel.status == status) \
        .all()


def fetch_all_candidates_from_vacancy(db: Session, vacancy: enums.Vacancies) -> List[CandidateModel]:
    return db.query(CandidateModel).filter(CandidateModel.vacancies.any(name=vacancy)).all()
