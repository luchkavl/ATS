from uuid import UUID

from fastapi import Path, Depends

import DB
from ats.exceptions import CandidateNotFoundException
from ats.models.general import Vacancies


def candidate_exists(candidate_id: UUID = Path(default=..., title="Candidate's UUID")) -> UUID:
    if candidate_id not in DB.CANDIDATES:
        raise CandidateNotFoundException(candidate_id)
    return candidate_id


class CommonPathParams:
    def __init__(self,
                 vacancy_name: Vacancies = Path(default=..., title='Vacancy'),
                 candidate_id: UUID = Depends(candidate_exists)
                 ):
        self.candidate_id = candidate_id
        self.vacancy_name = vacancy_name
