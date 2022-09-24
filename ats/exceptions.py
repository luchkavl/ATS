from uuid import UUID


class CandidateNotFoundException(Exception):
    def __init__(self, candidate_id: UUID):
        self.candidate_id = candidate_id
