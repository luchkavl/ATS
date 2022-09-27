import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ats.models.candidates import FullInfoCandidate, NeededInfoToCreateCandidate, NewCandidate, Feedback
import database.models as db_models
from database.schemas import CandidateInDB


def create_new_candidate(candidate_info: NeededInfoToCreateCandidate) -> NewCandidate:
    candidate_uuid = uuid.uuid4()

    new_candidate = NewCandidate(candidate_id=candidate_uuid, **candidate_info.dict())
    return new_candidate


def create_db_candidate(candidate) -> db_models.Candidate:
    candidate_in_db = CandidateInDB(**candidate.dict())
    db_candidate = db_models.Candidate(**candidate_in_db.dict())
    return db_candidate


def create_db_candidate_feedback(candidate_id: uuid.UUID, feedback: Feedback) -> db_models.CandidateFeedback:
    db_candidate_feedback = db_models.CandidateFeedback(candidate_id=candidate_id, **feedback.dict())
    return db_candidate_feedback
