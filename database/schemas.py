from uuid import UUID

from ats.models.candidates import CandidateID, CandidatePersonalInfo, CandidateStatus, FeedbackCreate
from ats.models.users import UserToDB


class CandidateInDB(CandidateID, CandidatePersonalInfo, CandidateStatus):
    class Config:
        orm_mode = True


class CandidateInDBUpdate(CandidatePersonalInfo, CandidateStatus):
    pass


class CreateDBFeedback(FeedbackCreate):
    candidate_id: UUID


class FeedbackInDB(CreateDBFeedback):
    id: int


class UserInDB(UserToDB):
    pass
