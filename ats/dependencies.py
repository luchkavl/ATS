from uuid import UUID

from fastapi import Path, Depends
from sqlalchemy.orm import Session

from ats.exceptions import CandidateNotFoundException
from ats.enums import Vacancies
from ats import crud
from database.db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def candidate_exists(candidate_id: UUID = Path(default=..., title="Candidate's UUID"),
                     db: Session = Depends(get_db)) -> UUID:
    if crud.get_candidate_by_id(db, candidate_id):
        return candidate_id
    else:
        raise CandidateNotFoundException(candidate_id)


class CommonPathParams:
    def __init__(self,
                 vacancy_name: Vacancies = Path(default=..., title='Vacancy'),
                 candidate_id: UUID = Depends(candidate_exists)
                 ):
        self.candidate_id = candidate_id
        self.vacancy_name = vacancy_name
