from typing import Union
import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ats.security import oauth2_scheme
from ats.dependencies import get_db, candidate_exists
from ats.models.candidates import AllCandidates, FullInfoCandidate, CandidatePersonalInfo, \
    NeededInfoToCreateCandidate, CandidateID
from ats import utils, enums
from ats import crud


router = APIRouter(
    prefix='/candidates',
    tags=[enums.Tags.candidates],
    dependencies=[Depends(oauth2_scheme)]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CandidateID)
async def create_candidate(candidate_info: NeededInfoToCreateCandidate, db: Session = Depends(get_db)):
    new_candidate = utils.create_new_candidate(candidate_info)
    crud.create_candidate(db, new_candidate)
    return {'candidate_id': new_candidate.candidate_id}


@router.get('/', response_model=AllCandidates)
async def read_all_candidates(
        candidates_status: enums.Statuses = Query(
            default=None, title="Candidate's status", description="Show candidates only with this status"),
        db: Session = Depends(get_db)
):
    if candidates_status:
        candidates = crud.get_all_candidates_by_status(db, candidates_status)
    else:
        candidates = crud.get_all_candidates(db)
    return AllCandidates(candidates=candidates)


@router.get('/{candidate_id}', response_model=Union[FullInfoCandidate, CandidatePersonalInfo])
async def read_candidate(
        candidate_id: uuid.UUID = Depends(candidate_exists),
        personal_info_only: bool = Query(
            default=None, alias='personal-info', title='Personal info',
            description="Show only candidate's personal info."),
        db: Session = Depends(get_db)
):
    candidate = crud.get_candidate_by_id(db, candidate_id)
    if personal_info_only:
        return CandidatePersonalInfo(**candidate.dict())
    return FullInfoCandidate(**candidate.dict())


@router.put('/{candidate_id}')
async def update_candidate_personal_info(*,
                                         candidate_id: uuid.UUID = Depends(candidate_exists),
                                         updated_candidate_info: CandidatePersonalInfo,
                                         db: Session = Depends(get_db)
                                         ):
    crud.update_candidate_personal_info(db, candidate_id, updated_candidate_info)
    return {}


@router.patch('/{candidate_id}/status')
async def change_candidate_status(
        candidate_id: uuid.UUID = Depends(candidate_exists),
        new_status: enums.Statuses = Query(title='Status', description="New candidate's status"),
        db: Session = Depends(get_db)
):
    crud.update_candidate_status(db, candidate_id, new_status)
    return {}


@router.delete('/{candidate_id}')
async def delete_candidate(candidate_id: uuid.UUID = Depends(candidate_exists), db: Session = Depends(get_db)):
    crud.delete_candidate(db, candidate_id)
    return {}
