from uuid import UUID
from pydantic import BaseModel, Field, EmailStr

from ats import enums


class CandidatePersonalInfo(BaseModel):
    first_name: str = Field(title="Candidate's first name", example='Ivan', max_length=50)
    last_name: str = Field(title="Candidate's last name", example='Ivanenko', max_length=50)
    email: EmailStr = Field(title="Candidate's email", example='123@google.com')


class CandidateStatus(BaseModel):
    status: enums.Statuses = Field(
        default=enums.Statuses.active,
        title='Status',
        description="Candidate's status",
        example='active')


class CandidateID(BaseModel):
    candidate_id: UUID = Field(title="Candidate's UUID", example='a3d00e4a-d2fe-4d35-b754-57f5a67b3b34')


class CandidateVacancies(BaseModel):
    vacancies: list[enums.Vacancies] = Field(
        title="Vacancies",
        description='Vacancies to which candidate qualified',
        example=['python'])


class FeedbackCreate(BaseModel):
    vacancy: enums.Vacancies = Field(title="Vacancy", example='python')
    stage: enums.InterviewStages = Field(title="Interview stage", example='hr')
    feedback_text: str = Field(title="Feedback text", example='Nice candidate.')


class Feedback(FeedbackCreate):
    id: int = Field(title="Feedback id", example='2')


class CandidateFeedbacks(BaseModel):
    feedbacks: list[Feedback] = Field(
        default=[],
        title='All feedbacks',
        example={'feedbacks': [
            {
                'id': '9',
                'vacancy': 'python',
                'stage': 'hr',
                'feedback_text': 'Nice.'
            }
        ]
        }
    )


class BaseCandidate(CandidateStatus, CandidatePersonalInfo):
    class Config:
        orm_mode = True


class NeededInfoToCreateCandidate(CandidateVacancies, BaseCandidate):
    pass


class NewCandidate(NeededInfoToCreateCandidate, CandidateID):
    pass


class FullInfoCandidate(CandidateFeedbacks, NewCandidate):
    pass


class AllCandidates(BaseModel):
    candidates: list[FullInfoCandidate | None] = Field(
        title="Candidates",
        example=[
            {
                "candidate_id": "a3d00e4a-d2fe-4d35-b754-57f5a67b3b34",
                "first_name": "Vladyslav",
                "last_name": "Luchka",
                "email": "vluchka@intelliarts.com",
                "status": "active",
                "vacancies": ["python"],
                "feedbacks": [
                    {
                        'id': '1',
                        'vacancy': 'python',
                        'stage': 'hr',
                        'feedback_text': 'Nice.'
                    }
                ]
            }
        ])

    class Config:
        schema_extra = {
            'example': {'candidates': [
                {
                    "candidate_id": "a3d00e4a-d2fe-4d35-b754-57f5a67b3b34",
                    "first_name": "Vladyslav",
                    "last_name": "Luchka",
                    "email": "vluchka@intelliarts.com",
                    "status": "active",
                    "vacancies": ["python"],
                    "feedbacks": [
                        {
                            'id': '14',
                            'vacancy': 'python',
                            'stage': 'hr',
                            'feedback_text': 'Nice.'
                        }
                    ]
                },
                {
                    "candidate_id": "2f89b7a2-7280-454b-8dd9-7d38add67d59",
                    "first_name": "Ivan",
                    "last_name": "Ivanov",
                    "email": "123@gmail.com",
                    "status": "active",
                    "vacancies": ["java"],
                    "feedbacks": [
                        {
                            'id': '1',
                            'vacancy': 'java',
                            'stage': 'hr',
                            'feedback_text': 'Nice.'
                        },
                        {
                            'id': '13',
                            'vacancy': 'java',
                            'stage': 'technical',
                            'feedback_text': 'Good.'
                        }
                    ]
                }
            ]}

        }
