from uuid import UUID, uuid4

import DB
from ats.models.candidates import FullInfoCandidate, NeededInfoToCreateCandidate, NewCandidate, CandidateToCandidates


def fetch_candidate_from_db(candidate_id: UUID) -> FullInfoCandidate:
    base_info = DB.CANDIDATES[candidate_id]
    vacancies = [vacancy for vacancy, candidates in DB.JOBS.items() if candidate_id in candidates]
    feedbacks = DB.FEEDBACKS.get(candidate_id) or {}

    candidate = FullInfoCandidate(vacancies=vacancies, feedbacks=feedbacks, **base_info)
    return candidate


def create_new_candidate(candidate_in: NeededInfoToCreateCandidate) -> NewCandidate:
    candidate_uuid = uuid4()

    new_candidate = NewCandidate(candidate_id=candidate_uuid, **candidate_in.dict())
    return new_candidate


def save_candidate_to_db(new_candidate: NewCandidate) -> None:
    cand_to_candidates = CandidateToCandidates(**new_candidate.dict())
    id_candidate_dict = {cand_to_candidates.candidate_id: cand_to_candidates.dict()}

    DB.CANDIDATES.update(id_candidate_dict)
    DB.STATUSES.update(cand_to_candidates.candidate_id)
    for vacancy in new_candidate.vacancies:
        DB.JOBS[vacancy].append(new_candidate.candidate_id)


def delete_candidate_from_db(candidate: FullInfoCandidate) -> None:
    del DB.CANDIDATES[candidate.candidate_id]
    if candidate.candidate_id in DB.FEEDBACKS:
        del DB.FEEDBACKS[candidate.candidate_id]
    for vacancy in candidate.vacancies:
        DB.JOBS[vacancy].remove(candidate.candidate_id)
