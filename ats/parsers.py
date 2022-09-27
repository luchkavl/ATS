from ats import enums
from ats.models.candidates import FullInfoCandidate, Feedback
from database.schemas import CandidateInDB
import database.models as db_models


def parse_db_candidate(db_full_info_candidate: db_models.Candidate) -> CandidateInDB:
    candidate_frm_db = CandidateInDB(
        candidate_id=db_full_info_candidate.id,
        first_name=db_full_info_candidate.first_name,
        last_name=db_full_info_candidate.last_name,
        email=db_full_info_candidate.email,
        status=db_full_info_candidate.status
    )
    return candidate_frm_db


def parse_db_candidate_vacancies(db_full_info_candidate: db_models.Candidate) -> list[enums.Vacancies]:
    vacancies = [vacancy.name for vacancy in db_full_info_candidate.vacancies]
    return vacancies


def _db_feedback_to_feedback(db_feedback: db_models.CandidateFeedback) -> Feedback:
    feedback = Feedback(
        vacancy=db_feedback.vacancy,
        stage=db_feedback.stage,
        feedback_text=db_feedback.feedback_text,
        id=db_feedback.id
    )
    return feedback


def parse_db_candidate_feedbacks(db_full_info_candidate: db_models.Candidate) -> list[Feedback]:
    feedbacks = []
    for db_feedback in db_full_info_candidate.feedbacks:
        feedback = _db_feedback_to_feedback(db_feedback)
        feedbacks.append(feedback)
    return feedbacks


def parse_full_info_candidate_from_db(db_full_info_candidate: db_models.Candidate) -> FullInfoCandidate:
    candidate_from_db = parse_db_candidate(db_full_info_candidate)
    vacancies = parse_db_candidate_vacancies(db_full_info_candidate)
    feedbacks = parse_db_candidate_feedbacks(db_full_info_candidate)

    candidate = FullInfoCandidate(**candidate_from_db.dict(), vacancies=vacancies, feedbacks=feedbacks)
    return candidate
