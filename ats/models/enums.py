from enum import Enum


class Tags(Enum):
    candidates = 'candidates'
    jobs = 'jobs'
    admin = 'admin'
    auth = 'auth'


class Vacancies(str, Enum):
    java = 'java'
    js = 'js'
    python = 'python'


class InterviewStages(str, Enum):
    hr = 'hr'
    technical = 'technical'
    offer = 'offer'


class Statuses(str, Enum):
    active = 'active'
    on_hold = 'on_hold'
    disqualified = 'disqualified'
