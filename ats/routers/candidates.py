from typing import Union
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status, HTTPException

import DB
from ats.models.general import Tags
from ats.security import oauth2_scheme
from ats.dependencies import candidate_exists
from ats.models.candidates import AllCandidates, Statuses, FullInfoCandidate, CandidatePersonalInfo, \
    NeededInfoToCreateCandidate, CandidateToUpdate
from ats.utils import fetch_candidate_from_db, create_new_candidate, save_candidate_to_db, delete_candidate_from_db

router = APIRouter(
    prefix='/candidates',
    tags=[Tags.candidates],
    dependencies=[Depends(oauth2_scheme)]
)


@router.get('/', response_model=AllCandidates, dependencies=[Depends(oauth2_scheme)])
async def read_all_candidates(candidates_status: Statuses = Query(
    default=None, title="Candidate's status", description="Show candidates only with this status")
):
    if candidates_status:
        candidates = [fetch_candidate_from_db(candidate_id) for candidate_id in DB.STATUSES[candidates_status]]
    else:
        candidates = [fetch_candidate_from_db(candidate_id) for candidate_id in DB.CANDIDATES.keys()]
    return AllCandidates(candidates=candidates)


@router.get('/{candidate_id}', response_model=Union[FullInfoCandidate, CandidatePersonalInfo])
async def read_candidate(
        candidate_id: UUID = Depends(candidate_exists),
        personal_info_only: bool = Query(
            default=None, alias='personal-info', title='Personal info',
            description="Show only candidate's personal info.")
):
    candidate = fetch_candidate_from_db(candidate_id)
    if personal_info_only:
        return CandidatePersonalInfo(**candidate.dict())
    return FullInfoCandidate(**candidate.dict())


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_candidate(candidate_info: NeededInfoToCreateCandidate):
    new_candidate = create_new_candidate(candidate_info)
    save_candidate_to_db(new_candidate)
    return {'candidate_id': new_candidate.candidate_id}


@router.put('/{candidate_id}')
async def update_candidate(*, candidate_id: UUID = Depends(candidate_exists),
                           updated_candidate_info: CandidateToUpdate):
    old_candidate = fetch_candidate_from_db(candidate_id)
    updated_candidate = FullInfoCandidate(candidate_id=candidate_id, **updated_candidate_info.dict())

    updated_candidate_vacancies = set(updated_candidate.vacancies)
    old_candidate_vacancies = set(old_candidate.vacancies)

    if added_vacancies := updated_candidate_vacancies.difference(old_candidate_vacancies):
        for vacancy in added_vacancies:
            DB.JOBS[vacancy].append(candidate_id)
    if deleted_vacancies := old_candidate_vacancies.difference(updated_candidate.vacancies):
        for vacancy in deleted_vacancies:
            DB.JOBS[vacancy].remove(candidate_id)

    return {}


@router.patch('/{candidate_id}/status')
async def change_candidate_status(
        candidate_id: UUID = Depends(candidate_exists),
        new_status: Statuses = Query(title='Status', description="New candidate's status")):
    candidate = fetch_candidate_from_db(candidate_id)
    if new_status == candidate.status:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    else:
        DB.STATUSES[candidate.status].remove(candidate_id)
        DB.STATUSES[new_status].append(candidate_id)
        return {}


@router.delete('/{candidate_id}')
async def delete_candidate(candidate_id: UUID = Depends(candidate_exists)):
    candidate = fetch_candidate_from_db(candidate_id)
    delete_candidate_from_db(candidate)
    return {}
