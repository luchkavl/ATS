from uuid import UUID

CANDIDATES = {
    UUID('a3d00e4a-d2fe-4d35-b754-57f5a67b3b34'): {
        'candidate_id': 'a3d00e4a-d2fe-4d35-b754-57f5a67b3b34',
        'first_name': 'Vladyslav',
        'last_name': 'Luchka',
        'email': 'vluchka@intelliarts.com',
    }
}

JOBS = {
    'java': [],
    'js': [],
    'python': [
        UUID('a3d00e4a-d2fe-4d35-b754-57f5a67b3b34')]
}

FEEDBACKS = {
    UUID('a3d00e4a-d2fe-4d35-b754-57f5a67b3b34'): {
        'python': {
            'hr': 'Nice'
        }
    }
}

STATUSES = {
    'active': [UUID('a3d00e4a-d2fe-4d35-b754-57f5a67b3b34')],
    'on_hold': [],
    'disqualified': []
}

USERS = {
    "luchka_vl": {
        "username": "luchka_vl",
        "full_name": "Vladyslav Luchka",
        "email": "vluchka@intelliarts.com",
        "hashed_password": "$2b$12$7aa9n.12VHelPfwSUbDbkeMzb5oDEV7AvIfL2lcuFZyAPhAVz1yg.",
        "admin": True,
    }
}
