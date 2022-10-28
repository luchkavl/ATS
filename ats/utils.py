import uuid

from ats.models.candidates import NeededInfoToCreateCandidate, NewCandidate, Feedback
from database.models import CandidateModel, CandidateFeedbackModel
from database.schemas import CandidateInDB


def create_new_candidate(candidate_info: NeededInfoToCreateCandidate) -> NewCandidate:
    candidate_uuid = uuid.uuid4()

    new_candidate = NewCandidate(candidate_id=candidate_uuid, **candidate_info.dict())
    return new_candidate


def create_db_candidate(candidate) -> CandidateModel:
    candidate_in_db = CandidateInDB(**candidate.dict())
    db_candidate = CandidateModel(**candidate_in_db.dict())
    return db_candidate


def create_db_candidate_feedback(candidate_id: uuid.UUID, feedback: Feedback) -> CandidateFeedbackModel:
    db_candidate_feedback = CandidateFeedbackModel(candidate_id=candidate_id, **feedback.dict())
    return db_candidate_feedback
