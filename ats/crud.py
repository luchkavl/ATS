import uuid
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from ats.models.candidates import NewCandidate, FullInfoCandidate, CandidatePersonalInfo
from ats import utils, enums
from ats.parsers import parse_full_info_candidate_from_db
from database import queries
from database.models import CandidateModel, CandidateFeedbackModel
from database.schemas import CreateDBFeedback


def add_new_candidate_to_vacancy(db: Session, candidate_to_db: CandidateModel, vacancy_name: enums.Vacancies) -> None:
    db_vacancy = queries.fetch_vacancy_by_name(db, vacancy_name)
    db_vacancy.candidates.append(candidate_to_db)


def create_candidate(db: Session, candidate: NewCandidate) -> None:
    db_candidate = utils.create_db_candidate(candidate)
    db.add(db_candidate)

    for vacancy_name in candidate.vacancies:
        add_new_candidate_to_vacancy(db, db_candidate, vacancy_name)

    db.commit()


def _parse_db_candidates(db_full_info_candidates: List[CandidateModel]) -> List[FullInfoCandidate]:
    candidates = []
    for db_full_info_candidate in db_full_info_candidates:
        candidate = parse_full_info_candidate_from_db(db_full_info_candidate)
        candidates.append(candidate)
    return candidates


def get_all_candidates(db: Session) -> List[FullInfoCandidate]:
    db_full_info_candidates = queries.fetch_all_full_info_candidates(db)
    candidates = _parse_db_candidates(db_full_info_candidates)
    return candidates


def get_all_candidates_by_status(db: Session, status: enums.Statuses) -> List[FullInfoCandidate]:
    db_full_info_candidates = queries.fetch_full_info_candidates_by_status(db, status)
    candidates = _parse_db_candidates(db_full_info_candidates)
    return candidates


def get_candidate_by_id(db: Session, candidate_id: uuid.UUID) -> FullInfoCandidate:
    db_full_info_candidate = queries.fetch_full_info_candidate_by_id(db, candidate_id)
    candidate = parse_full_info_candidate_from_db(db_full_info_candidate)
    return candidate


def delete_candidate(db: Session, candidate_id: uuid.UUID) -> None:
    db_full_info_candidate = queries.fetch_full_info_candidate_by_id(db, candidate_id)
    db.delete(db_full_info_candidate)
    db.commit()


def update_candidate_personal_info(
        db: Session, candidate_id: uuid.UUID, updated_candidate_info: CandidatePersonalInfo) -> None:
    db_base_info_candidate = queries.fetch_base_info_candidate_by_id(db, candidate_id)

    db_base_info_candidate.first_name = updated_candidate_info.first_name
    db_base_info_candidate.last_name = updated_candidate_info.last_name
    db_base_info_candidate.email = updated_candidate_info.email
    db.commit()


def update_candidate_status(db: Session, candidate_id: uuid.UUID, new_status: enums.Statuses) -> None:
    db_base_info_candidate = queries.fetch_base_info_candidate_by_id(db, candidate_id)
    if db_base_info_candidate.status == new_status:
        raise HTTPException(
            status_code=304, detail=f'Candidate with id {str(candidate_id)} already has status {new_status}')
    else:
        db_base_info_candidate.status = new_status
        db.commit()


def get_all_candidates_from_vacancy(
        db: Session,
        vacancy_name: enums.Vacancies, by_candidates_status: enums.Statuses | None = None) -> List[FullInfoCandidate]:
    if by_candidates_status:
        db_candidates = queries.fetch_all_candidates_by_vacancy_status(db, vacancy_name, status=by_candidates_status)
    else:
        db_candidates = queries.fetch_all_candidates_from_vacancy(db, vacancy_name)
    candidates = _parse_db_candidates(db_candidates)
    return candidates


def create_candidate_feedback(db: Session, feedback: CreateDBFeedback) -> CandidateFeedbackModel.id:
    feedback_to_db = CandidateFeedbackModel(**feedback.dict())
    db.add(feedback_to_db)
    db.commit()

    feedback_id = feedback_to_db.id
    return feedback_id


def delete_candidate_from_vacancy(db: Session, vacancy_name: enums.Vacancies, candidate_id: uuid.UUID) -> None:
    vacancy = queries.fetch_vacancy_by_name(db, vacancy_name)
    candidate: CandidateModel = queries.fetch_full_info_candidate_by_id(db, candidate_id)
    vacancy.candidates.remove(candidate)
    db.commit()
