from fastapi import APIRouter, Path, Query, status, Body, Depends, Form

import DB
from ats.security import oauth2_scheme
from ats.dependencies import CommonPathParams
from ats.models.candidates import AllCandidates, Vacancies, Statuses, BaseCandidate, NeededInfoToCreateCandidate, \
    InterviewStages
from ats.models.enums import Tags
from ats.utils import fetch_candidate_from_db, create_new_candidate, save_candidate_to_db, delete_candidate_from_db

router = APIRouter(
    prefix='/jobs',
    tags=[Tags.jobs],
    dependencies=[Depends(oauth2_scheme)]
)


@router.get('/{vacancy_name}/candidates/', response_model=AllCandidates)
async def read_all_candidates_from_vacancy(
        vacancy_name: Vacancies = Path(
            default=..., title='Vacancy', description='Vacancy from which to show all candidates'),
        candidates_status: Statuses = Query(
            default=None, title="Candidate's status", description="Show candidates only with this status")
):
    if candidates_status:
        candidates = []
        for candidate_id in DB.JOBS[vacancy_name]:
            if candidate_id in DB.STATUSES[candidates_status]:
                candidate = fetch_candidate_from_db(candidate_id)
                candidates.append(candidate)
    else:
        candidates = [fetch_candidate_from_db(candidate_id) for candidate_id in JOBS[vacancy_name]]
    return AllCandidates(candidates=candidates)


@router.post('/{vacancy_name}/candidates/', status_code=status.HTTP_201_CREATED)
async def create_candidate_to_vacancy(
        vacancy_name: Vacancies = Path(
            default=..., title='Vacancy', description='Vacancy to which add the candidate'),
        candidate: BaseCandidate = Body(
            default=..., title='Basic info', description="Candidate's personal info and status")
):
    vacancies = [vacancy_name]
    candidate_info = NeededInfoToCreateCandidate(vacancies=vacancies, **candidate.dict())

    new_candidate = create_new_candidate(candidate_info)
    save_candidate_to_db(new_candidate)
    return {'candidate_id': new_candidate.candidate_id}


@router.post('/{vacancy_name}/stages/{stage_name}/candidates/{candidate_id}',
             status_code=status.HTTP_201_CREATED)
async def add_feedback(
        commons: CommonPathParams = Depends(),
        stage_name: InterviewStages = Path(
            default=..., title='Stage', description="Interview stage on which add the feedback"),
        feedback: str = Form(default=..., min_length=1, max_length=512)
):
    DB.FEEDBACKS[commons.candidate_id][commons.vacancy_name][stage_name] = feedback
    return {}


@router.delete('/{vacancy_name}/candidates/{candidate_id}')
async def remove_candidate_from_vacancy(commons: CommonPathParams = Depends()):
    candidate = fetch_candidate_from_db(commons.candidate_id)

    if len(candidate.vacancies) > 1:
        DB.JOBS[commons.vacancy_name].remove(commons.candidate_id)
        DB.FEEDBACKS[commons.candidate_id].pop(commons.vacancy_name)
        return fetch_candidate_from_db(commons.candidate_id)
    else:
        delete_candidate_from_db(candidate)
        return {}
