from fastapi import APIRouter, Path, Query, status, Body, Depends, Form
from sqlalchemy.orm import Session

from ats import crud, utils, enums
from ats.security import oauth2_scheme
from ats.dependencies import CommonPathParams, get_db
from ats.models.candidates import AllCandidates, BaseCandidate, NeededInfoToCreateCandidate
from database.schemas import CreateDBFeedback

router = APIRouter(
    prefix='/vacancies',
    tags=[enums.Tags.jobs],
    dependencies=[Depends(oauth2_scheme)]
)


@router.get('/{vacancy_name}/candidates/', response_model=AllCandidates)
async def read_all_candidates_from_vacancy(
        vacancy_name: enums.Vacancies = Path(
            default=..., title='Vacancy', description='Vacancy from which to show all candidates'),
        candidates_status: enums.Statuses = Query(
            default=None, title="Candidate's status", description="Show candidates only with this status"),
        db: Session = Depends(get_db)
):
    candidates = crud.get_all_candidates_from_vacancy(db, vacancy_name, by_candidates_status=candidates_status)
    return AllCandidates(candidates=candidates)


@router.post('/{vacancy_name}/candidates/', status_code=status.HTTP_201_CREATED)
async def create_candidate_to_vacancy(
        vacancy_name: enums.Vacancies = Path(
            default=..., title='Vacancy', description='Vacancy to which add the candidate'),
        candidate: BaseCandidate = Body(
            default=..., title='Basic info', description="Candidate's personal info and status"),
        db: Session = Depends(get_db)
):
    candidate_info = NeededInfoToCreateCandidate(vacancies=[vacancy_name], **candidate.dict())

    new_candidate = utils.create_new_candidate(candidate_info)
    crud.create_candidate(db, new_candidate)
    return {'candidate_id': new_candidate.candidate_id}


@router.post('/{vacancy_name}/stages/{stage_name}/candidates/{candidate_id}/feedbacks/',
             status_code=status.HTTP_201_CREATED)
async def add_vacancy_stage_candidate_feedback(
        commons: CommonPathParams = Depends(),
        stage_name: enums.InterviewStages = Path(
            default=..., title='Stage', description="Interview stage on which add the feedback"),
        feedback_text: str = Form(default=..., min_length=1, max_length=512),
        db: Session = Depends(get_db)
):
    feedback_to_save = CreateDBFeedback(
        vacancy=commons.vacancy_name, stage=stage_name, candidate_id=commons.candidate_id, feedback_text=feedback_text)
    feedback_id = crud.create_candidate_feedback(db, feedback_to_save)

    return {'feedback_id': feedback_id}


@router.delete('/{vacancy_name}/candidates/{candidate_id}')
async def remove_candidate_from_vacancy(commons: CommonPathParams = Depends(), db: Session = Depends(get_db)):
    crud.delete_candidate_from_vacancy(db, commons.vacancy_name, commons.candidate_id)
    return {}
