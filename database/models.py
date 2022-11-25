import uuid
from sqlalchemy import Column, String, Enum, ForeignKey, Text, Boolean, Table, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ats import enums
from database.db import Base

candidate_vacancies = Table('candidate_vacancies', Base.metadata,
                            Column('candidate_id', ForeignKey('candidates.candidate_id'), primary_key=True),
                            Column('vacancy', ForeignKey('jobs.name'), primary_key=True)
                            )


class CandidateModel(Base):
    __tablename__ = 'candidates'

    candidate_id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    status = Column(Enum(enums.Statuses))
    vacancies = relationship('VacancyModel', secondary=candidate_vacancies, back_populates='candidates')
    feedbacks = relationship('CandidateFeedbackModel', cascade="all, delete-orphan")


class VacancyModel(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(enums.Vacancies), unique=True, primary_key=True)
    candidates = relationship('CandidateModel', secondary=candidate_vacancies, back_populates='vacancies')


class CandidateFeedbackModel(Base):
    __tablename__ = 'candidate_feedbacks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey('candidates.candidate_id'))
    vacancy = Column(Enum(enums.Vacancies), ForeignKey('jobs.name'))
    stage = Column(Enum(enums.InterviewStages))
    feedback_text = Column(Text, nullable=False)


class UserModel(Base):
    __tablename__ = 'users'

    username = Column(String, unique=True, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    admin = Column(Boolean, nullable=False)
