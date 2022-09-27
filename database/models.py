import uuid
from sqlalchemy import Column, String, Enum, ForeignKey, Text, Boolean, Table, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ats import enums
from database.db import Base

candidate_vacancies = Table('candidate_vacancies', Base.metadata,
                            Column('candidate_id', ForeignKey('candidates.id'), primary_key=True),
                            Column('vacancy', ForeignKey('jobs.name'), primary_key=True)
                            )


class Candidate(Base):
    __tablename__ = 'candidates'

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    status = Column(Enum(enums.Statuses))
    vacancies = relationship('Vacancy', secondary=candidate_vacancies, back_populates='candidates')
    feedbacks = relationship('CandidateFeedback', cascade="all, delete-orphan")

    def __init__(self, candidate_id, first_name, last_name, email, status):
        self.id = candidate_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.status = status


class Vacancy(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(enums.Vacancies), unique=True, primary_key=True)
    candidates = relationship('Candidate', secondary=candidate_vacancies, back_populates='vacancies')

    def __init__(self, name: enums.Vacancies):
        self.name = name


class CandidateFeedback(Base):
    __tablename__ = 'candidate_feedbacks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey('candidates.id'))
    vacancy = Column(Enum(enums.Vacancies), ForeignKey('jobs.name'))
    stage = Column(Enum(enums.InterviewStages))
    feedback_text = Column(Text)

    def __init__(self, candidate_id, vacancy, stage, feedback_text):
        self.candidate_id = candidate_id
        self.vacancy = vacancy
        self.stage = stage
        self.feedback_text = feedback_text


class User(Base):
    __tablename__ = 'users'

    username = Column(String, unique=True, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    admin = Column(Boolean)

    def __init__(self, username, full_name, email, hashed_password, admin):
        self.username = username
        self.full_name = full_name
        self.email = email
        self.hashed_password = hashed_password
        self.admin = admin
