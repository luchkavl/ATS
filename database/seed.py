from ats import enums
from database.db import Base, engine, SessionLocal
from database.models import VacancyModel, UserModel

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    for vacancy_name in enums.Vacancies:
        session.add(VacancyModel(name=enums.Vacancies[vacancy_name]))

    admin = UserModel(username='admin',
                      full_name='admin',
                      email='admin@example.com',
                      hashed_password="$2b$12$idQNwDj5bDgo5QfrKFP0WeIYE505iEE0miJoQAdgB7mKYRc7IJQD2",
                      admin=True)
    session.add(admin)

    session.commit()
    session.close()
